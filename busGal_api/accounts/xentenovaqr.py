from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import XG_XNQR_APP as BASE_URL
from ..exceptions import TPGalWSBadJsonException, TPGalWSAppException
from .qrutils import create_qr as _create_qr
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import textwrap


_rest_adapter = RestAdapter(BASE_URL)


def _authentication_function():
    response = _rest_adapter.post("/LoginApp/authenticate",
                                  data={"username": "apixnv",
                                        "password": "*jhFUhDiAurAls&jsuEJsPcbAsae*"}, load_json=False)  # This is hardcoded into the app

    return response.text


# Here tokens actually expire after some time, unlike in the TPGAL accounts
_rest_adapter._authentication_function = _authentication_function


class Qr():
    """
    Class that represents a QR code used to pay in the bus. On creation, if `data` is not set, it will query the api to get the neccesary parameters for a new QR (`id_account`, `id_account_product` and `device_id` are needed), and call `Qr.refresh_qr_string` if the qr's status is 'pending'. Keep in mind that, in the app, QRs are updated locally every 30s (check the source of `busGal_api.accounts.qrutils` if curious how), therefore you *should* run `Qr.refresh_qr_string` every 30s and update your image accordingly. Also, they seem to become invalid after 5min. Keep in mind I haven't tested any edge cases or tried to avoid these limits.

    :param id_account: See `Account.id_account`
    :param id_account_product: See `Account.id_account_product`
    :param device_id: See `Account.device_id`
    :param data: See the source code. The json data for a QR returned by the API
    """

    def __init__(self, id_account: int = None, id_account_product: int = None, device_id: int = None, data: dict = None):
        if data:
            pass
        elif id_account and id_account_product and device_id:
            data = _rest_adapter.post("/Qr",
                                      data={"destinationCode": 9999,
                                            "destinationName": "",
                                            "idAccount": id_account,
                                            "idAccountProduct": id_account_product,
                                            "idDevice": device_id,
                                            "originCode": 9999,
                                            "originName": "",
                                            "validityStartDateTime": datetime.now().strftime("%Y-%m-%d 00:00:00")})
        else:
            raise TypeError(
                "Qr.__init__() expected either the 'data' or all 3 `id_account`, `id_account_product` and `device_id` arguments")

        self.data = data
        """
        All the data the api provides (or was passed) in a dict
        """

        self.id_signature_keys = self.data["idSignatureKeys"]
        """
        Which of the keys in `busGal_api.accounts.accounts.qrutils.map_public_key_XN` (1-indexed) to use

        :type: int
        """

        self.static_data = self.data["staticData"]
        """
        The data at the start of the QR string that doesn't change
        """

        self.id = self.data["idQr"]
        """
        The id of the QR
        """

        self.origin_code = self.data["originCode"]
        """
        I haven't found any value in the TPGAL API that matches this
        """

        self.destination_code = self.data["destinationCode"]
        """
        I haven't found any value in the TPGAL API that matches this either
        """

        self.origin_stop_name = self.data["originStopName"]
        """
        Name of the stop where you took the bus
        """

        self.destination_stop_name = self.data["destinationStopName"]
        """
        Name of the stop to which you were going
        """

        self.update_date = datetime.strptime(
            self.data["updateDate"].split(".")[0], "%Y-%m-%dT%H:%M:%S")  # I split at the dot, because the microseconds? after aren't important in the app, and it doesn't work with %f
        """
        The app uses this to show when you paid the bus
        """

        self.status = self.data["status"]
        """
        The status of the QR It takes values from 1-5. The app only shows QRs with status 2,3 or 4. After the decompiling the app, we see the following constants have assigned each value (and they explain roughly what each value means):
        1. STATUS_QR_XN_PENDING
        2. STATUS_QR_XN_VALIDATED
        3. STATUS_QR_XN_VALIDATE_TRANSFER (not used), STATUS_QR_XN_CONSOLIDATED
        4. STATUS_QR_XN_EXPIRED (not used), STATUS_QR_XN_CONSOLIDATED_TRANSFER
        5. STATUS_QR_XN_REVOKE
        """

        if self.status == 1:
            self.refresh_qr_string()

    def refresh_qr_string(self):
        """
        Will update the QR, with the current time, encoded at the end. This is done every 30s in the app
        """

        self.qr_string = _create_qr(self.id_signature_keys, self.static_data)
        """
        The actual string you should put in your QR. Keep in mind that a `M` error correction level is used in the app
        """

        return self.qr_string

    def __repr__(self) -> str:
        return self.update_date.strftime("%Y-%m-%d %H:%M:%S")


class Account():
    """
    Class that represents a XenteNovaQR account. On creation the account will be fetched from the API

    :param external_user_id: Coincides with `busGal_api.accounts.Account.user_id`
    """

    def __init__(self, external_user_id: int):
        self.external_user_id = external_user_id
        """
        Id of the TPGAL account associated with this XenteNovaQR account
        """

        self.refresh_data()

    def refresh_data(self) -> None:
        """
        Refresh the account data from the API
        """

        self.data = _rest_adapter.get("/Account",
                                      ep_params={"idAccountExternalApp": self.external_user_id})[0]  # It returns a list with just one account
        """
        All the data the api provides in a dict (only the things I consider 'important' are set as attributes in this class)
        """

        self.balance = self.data["accountProducts"][0]["balance"]
        """
        The number of tickets you have left for this month
        """

        self.device_id = self.data["idDevice"]
        """
        The android_id corresponding to the TPGAL app on the device. See [this](https://developer.android.com/reference/android/provider/Settings.Secure.html#ANDROID_ID). The XNAccount's idDevice should be set to this (use `set_device_id`) or you'll get an error.
        """

        self.id_account = self.data["idAccount"]
        """
        The id of your account
        """

        self.id_account_product = self.data["accountProducts"][0]["idAccountProduct"]
        """
        Not sure what this actually means, but it is used for QR code creation
        """

        self.email = self.data["email"]
        """
        The email of the account
        """

        self.external_user_id = self.data["idAccountExternalApp"]

    def check_device(self, device_id: str) -> bool:
        """
        Check with the server if the given device matches the account (the app does this every time you open it to prevent it being used in two phones at the same time). Returns `True` if it matches

        :param device_id: See `Account.device_id` 
        """

        try:
            _rest_adapter.get("/Account",
                              ep_params={"idAccountExternalApp": self.external_user_id,
                                         "idDevice": device_id})
        except TPGalWSAppException as e:
            if e.app_error.code == 1:
                return False
            raise e

        return True

    def set_device_id(self, device_id: str) -> None:
        """
        Change the device id associated to the account

        :param device_id: See `Account.device_id`
        """
        _data = self.data
        _data["idDevice"] = device_id

        _rest_adapter.patch("/Account",
                            ep_params={
                                "idAccountExternalApp": self.external_user_id},
                            data=_data)

        self.refresh_data()

    def get_qrs(self, from_date: date = date.today() - relativedelta(months=1), to_date: date = date.today()) -> list[Qr]:
        """
        Search all generated Qrs for this account between the given dates

        :param from_date: Start of the search
        :param to_date: End of the search
        """
        qrs_data = _rest_adapter.get("/Qr",
                                     ep_params={"idAccount": self.id_account,
                                                "idDevice": self.device_id,  # Not actually needed
                                                "dateIni": from_date.strftime("%Y-%m-%d"),
                                                "dateEnd": to_date.strftime("%Y-%m-%d"),
                                                "idProduct": 1})

        qrs = [Qr(data=d) for d in qrs_data]

        return qrs

    def create_qr(self) -> Qr:
        """
        Wrapper to create a Qr object with this account's data
        """

        return Qr(self.id_account, self.id_account_product, self.device_id)

    def __repr__(self) -> str:
        return self.email


def register_account(name: str, birth_date: date, email: str, identity_number: str, identity_front_img: str, identity_rear_img: str, external_user_id: int, device_id: str) -> None:
    """
    Register an user account. You need a normal TPGAL account first. Keep in mind that, in the app, OCR is used for the verification process, so please don't use this to skip their measures and do not abuse the service.

    :param name: First name
    :param birth_date: Birth date
    :param email: Email address
    :param identity_number: Identity number e.g. your DNI
    :param identity_front_img: A photo of front of your Id Document. In base64
    :param identity_rear_img: A photo of rear of your Id Document. In base64
    :param external_user_id: See `Account.external_user_id`
    :param device_id: See `Account.device_id`
    """

    _rest_adapter.post("/Account",
                       data={
                           "birthDate": birth_date.strftime("%Y-%m-%d"),
                           "email": email,
                           "frontIdentityDocumentPhoto": textwrap.fill(identity_front_img, 76)+"\n",
                           "idAccountExternalApp": external_user_id,
                           "idDevice": device_id,
                           "idProductList": [],
                           "identityDocumentNumber": identity_number,
                           "name": name,
                           "rearIdentityDocumentPhoto": textwrap.fill(identity_rear_img, 76)+"\n",
                           "surname": ""
                       })
