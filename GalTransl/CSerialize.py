import json
import string

from GalTransl.CSentense import CTransList


def save_transList_to_json_cn(trans_list: CTransList, save_path: str, name_dict={}):
    result_list = []
    for tran in trans_list:
        if tran._speaker != "":
            if type(tran._speaker) == list:
                result_name = []
                for name in tran._speaker:
                    result_name.append(name_dict[name] if name in name_dict else name)
                result_list.append({"names": result_name, "message": tran.post_zh})
            else:
                result_name = (
                    name_dict[tran._speaker]
                    if tran._speaker in name_dict
                    else tran._speaker
                )
                result_list.append({"name": result_name, "message": tran.post_zh})
        else:
            result_list.append({"message": tran.post_zh})
    with open(save_path, "w", encoding="utf8") as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)


def update_json_with_transList_origin(
    trans_list: CTransList, old_json_list: list, name_dict={}
) -> list:
    result_json_list = old_json_list.copy()
    # Iterate over the old JSON data and the trans_list simultaneously
    for old_item, tran in zip(result_json_list, trans_list):
        # Check if the 'message' in the old JSON data matches with 'pre_jp' in the tran
        if old_item.get("message") == tran.pre_jp:
            # Update the 'message' field
            old_item["message"] = tran.post_zh

            # Update the 'name' field if it exists and tran._speaker is not a list
            if "name" in old_item and not isinstance(tran._speaker, list):
                old_item["name"] = (
                    name_dict[tran._speaker]
                    if tran._speaker in name_dict
                    else tran._speaker
                )

            # Update the 'names' field if it exists and tran._speaker is a list
            if "names" in old_item and isinstance(tran._speaker, list):
                old_item["names"] = [
                    name_dict[name] if name in name_dict else name
                    for name in tran._speaker
                ]

    return result_json_list


def update_json_with_transList(
    trans_list: CTransList, old_json_list: list, name_dict={}
) -> dict[string, string]:
    # TSK translation stored in Key Value JSON {"こんにちは": "你好"}
    kv = {}
    for tran in trans_list:
        kv[tran.pre_jp] = tran.post_zh

    return kv


def save_json(file_path: str, result_json: dict[string, string] | list):
    with open(file_path, "w", encoding="utf8", newline="\n") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=4)
