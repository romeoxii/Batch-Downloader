import requests


def is_file_or_folder(url):
        res = requests.get(url, stream=True)
        code = res.status_code
        reason = res.reason
        c_type = res.headers.get("Content-Type")
        if c_type == None:
            return
             
        media_type = c_type.split("/")[0]

        res.close()


        # check if url is good before deciding if it's file or folder
        if 200 <= code <=299:
            if media_type == "text":
                print("c type: ", c_type)
                print("media type: ", media_type)
                print("code: ", code)
                return "folder"
            else:
                print("c type: ", c_type)
                print("media type: ", media_type)
                print("code: ", code)
                return "file"
        else:
            return f"{code}: {reason}"


        