import logging

from utils import LogHandler
from base64 import b64decode, urlsafe_b64decode
from helpers import string_hash_code

handler = LogHandler()
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.INFO)


def Landroid_util_Base64_decode(params: list, vm, v: list):
    # add missing padding because python has very strong opinions about this
    v[params[0]] += [61] * (-len(v[params[0]]) % 4)
    # also sanitize the input by turning everything to bytes
    try:
        if len(params) == 1:
            vm.memory.last_return = list(b64decode(bytes(v[params[0]])))
        else:
            # check for URL safe base64 decode (that's how people usually use the flag)
            vm.memory.last_return = list(urlsafe_b64decode(bytes(v[params[0]])))
    except:
        # pokemoning the exception for the fallback for weird string formats
        vm.memory.last_return = list(b64decode("".join([chr(x) for x in v[params[0]]])))


def Landroid_view_TextUtils_isEmpty(params: list, vm, v: list):
    try:
        vm.memory.last_return = v[params[0]] is None or len(v[params[0]]) > 0
    except Exception:
        vm.memory.last_return = 0


def Ljava_io_ByteArrayOutputStream_0init0(params: list, vm, v: list):
    v[params[0]] = []


def Ljava_io_ByteArrayOutputStream_write(params: list, vm, v: list):
    v[params[0]].append(v[params[1]])


def Ljava_io_ByteArrayOutputStream_toByteArray(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]]


def Ljava_lang_Object_hashCode(params: list, vm, v: list):
    vm.memory.last_return = string_hash_code(v[params[0]].decode("utf-8"))


def Ljava_lang_String_0init0(params: list, vm, v: list):
        try:
            v[params[0]] = bytearray(v[params[1]]).decode("utf-8")
        except ValueError as ve:
            # got negative bytes (which somehow work in java land), need to strip the sign
            ret = []
            for b in v[params[1]]:
                if b < 0:
                    b += 0xFF + 1
                ret.append(b)
            v[params[0]] = bytearray(ret).decode("utf-8", "ignore")

        log.info(f"String created: {v[params[0]]}")


def Ljava_lang_String_charAt(params: list, vm, v: list):
    try:
        vm.memory.last_return = ord(v[params[0]].decode("utf-8", "surrogatepass")[v[params[1]]])
    except AttributeError as ae:
        try:
            vm.memory.last_return = ord(v[params[0]][v[params[1]]])
        except TypeError as te:
            vm.memory.last_return = v[params[0]][v[params[1]]]


def Ljava_lang_String_split(params: list, vm, v: list):
    vm.memory.last_return = str(v[params[0]]).split(str(v[params[1]]))


def Ljava_lang_String_equals(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]] == v[params[1]]


def Ljava_lang_String_length(params: list, vm, v: list):
    # TODO: remove catch all
    try:
        vm.memory.last_return = len(v[params[0]].decode("utf-8"))
    except AttributeError as ex:
        # TODO: remove catch all
        try:
            vm.memory.last_return = len(v[params[0]])
        except:
            vm.memory.last_return = 0
    except Exception as ex:
        vm.memory.last_return = 0


def Ljava_lang_String_indexOf(params: list, vm, v: list):
    # TODO: account for char substring
    try:
        vm.memory.last_return = v[params[0]].find(chr(v[params[1]]))
    except TypeError as te:
        # sometimes we get substrings, sometimes we get char codes
        vm.memory.last_return = str(v[params[0]]).find(str(v[params[1]]))
    except Exception as ex:
        # TODO: remove catch all
        vm.memory.last_return = 0


def Ljava_lang_String_valueOf(params: list, vm, v: list):
    vm.memory.last_return = chr(v[params[0]])


def Ljava_lang_String_toLowerCase(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]].lower()


def Ljava_lang_String_getBytes(params: list, vm, v: list):
    # TODO: standardize string passing across methods
    try:
        vm.memory.last_return = list(v[params[0]].encode("utf-8"))
    except:
        vm.memory.last_return = list(v[params[0]])


def Ljava_lang_StringBuilder_0init0(params: list, vm, v: list):
    if len(params) > 1:
        if isinstance(v[params[1]], list):
            v[params[0]] = ''.join(chr(i) for i in v[params[1]])
        if isinstance(v[params[1]], str):
            v[params[0]] = v[params[1]]
    else:
        v[params[0]] = ''
    log.info(f"String created: {v[params[0]]}")


def Ljava_lang_StringBuilder_append(params: list, vm, v: list):
    # TODO: maybe find a more elegant solution
    try:
        v[params[0]] = str(v[params[0]]) + chr(v[params[1]])
    except TypeError as te:
        try:
            v[params[0]] = str(v[params[0]]) + v[params[1]].decode("utf-8")
        except AttributeError as ae:
            v[params[0]] = str(v[params[0]]) + str(v[params[1]])


def Ljava_lang_StringBuilder_length(params: list, vm, v: list):
    try:
        vm.memory.last_return = len(v[params[0]])
    except Exception:
        # TODO: remove catch all
        vm.memory.last_return = 0

def Ljava_lang_StringBuilder_toString(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]]
    log.info(f"String created: {v[params[0]]}")


def Ljava_lang_StringBuffer_0init0(params: list, vm, v: list):
    if isinstance(v[params[1]], list):
        v[params[0]] = ''.join(chr(i) for i in v[params[1]])
    if isinstance(v[params[1]], str):
        v[params[0]] = v[params[1]]
    log.info(f"String created: {v[params[0]]}")


def Ljava_lang_StringBuffer_toString(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]]


def Ljava_util_Iterator_hasNext(params: list, vm, v: list):
    vm.memory.last_return = False


def Ljava_util_ArrayList_0init0(params: list, vm, v: list):
    v[params[0]] = []


def Ljava_util_ArrayList_size(params: list, vm, v: list):
    vm.memory.last_return = len(v[params[0]])


def Ljava_util_ArrayList_add(params: list, vm, v: list):
    # hack to quickly whip up a list
    if not v[params[0]]:
        v[params[0]] = []
    v[params[0]].append(v[params[1]])


def Ljava_util_ArrayList_get(params: list, vm, v: list):
    vm.memory.last_return = v[params[0]][v[params[1]]]


def Ljava_util_List_0init0(params: list, vm, v: list):
    v[params[0]] = []


def Ljava_util_List_size(params: list, vm, v: list):
    if isinstance(v[params[0]], list):
        vm.memory.last_return = len(v[params[0]])
    else:
        vm.memory.last_return = 0


def Ljavax_crypto_spec_SecretKeySpec_0init0(params: list, vm, v: list):
    pass


def try_to_mock_method(method_idx: int, params: list, vm, v) -> bool:
    class_name: str = vm.dex.method_ids[method_idx].class_name
    method_name: str = vm.dex.method_ids[method_idx].method_name
    log.debug("Translating method: %s->%s with %s" % (
        class_name, method_name, [str(v[param])[0:8] for param in params]))

    fqcn = class_name.replace('/', '_').replace(';', '') + '_' + method_name.replace('<', '0').replace('>', '0')

    fp = globals().get(fqcn, None)

    if fp:
        fp(params, vm, v)
        return False
    elif class_name == "Landroid/view/Display;":
        vm.memory.last_return = 0
        return False
    else:
        if any([x in method_name for x in ["Int", "Long", "Float"]]) and "get" in method_name:
            vm.memory.last_return = 0
            return False
        if "String" in method_name and "get" in method_name and len(method_name) > 9:
            vm.memory.last_return = "None"
            return False

    return True