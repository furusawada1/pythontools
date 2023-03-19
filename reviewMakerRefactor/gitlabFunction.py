import json
import zipfile
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
class GitLabAPI:
    def __init__(self, project_id, access_token):
        self.project_id = project_id
        self.access_token = access_token
        self.api_base_url = f"https://gitlab.com/api/v4/projects/{project_id}"
        self.headers = {
            "PRIVATE-TOKEN": access_token,
            "Content-Type": "application/json",
        }

    def get_diff_data(self, from_hash, to_hash):
        try:
            diff_url = f"{self.api_base_url}/repository/compare?from={from_hash}&to={to_hash}"
            diff_request = Request(diff_url, headers=self.headers)
            response = urlopen(diff_request)
            return json.loads(response.read())
        except HTTPError as e:
            print(f"HTTPエラー: {e.code} URL: {diff_url}")
        except URLError as e:
            print(f"URLエラー: {e.reason}")

    def fetch_files_from_gitlab(self, from_hash, to_hash, output_zip):
        diff_data = self.get_diff_data(from_hash, to_hash)

        if diff_data:
            with zipfile.ZipFile(output_zip, "w") as zf:
                for change in diff_data["diffs"]:
                    if change["new_file"] or change["renamed_file"]:
                        file_path = change["new_path"]
                        try:
                            file_url = f"{self.api_base_url}/repository/files/{quote(file_path, safe='')}/raw?ref={to_hash}"
                            file_request = Request(file_url, headers=self.headers)
                            file_response = urlopen(file_request)
                            file_content = file_response.read()
                            zf.writestr(file_path, file_content)
                        except HTTPError as e:
                            print(f"HTTPエラー: {e.code} URL: {file_url}")
                        except URLError as e:
                            print(f"URLエラー: {e.reason}")

    def get_project_data(self):
        try:
            project_url = f"{self.api_base_url}"
            project_request = Request(project_url, headers=self.headers)
            response = urlopen(project_request)
            return json.loads(response.read())
        except HTTPError as e:
            print(f"HTTPエラー: {e.code}")
        except URLError as e:
            print(f"URLエラー: {e.reason}")

    def get_merge_request_data(self, merge_request_id):
        try:
            mr_url = f"{self.api_base_url}/merge_requests/{merge_request_id}"
            mr_request = Request(mr_url, headers=self.headers)
            response = urlopen(mr_request)
            return json.loads(response.read())
        except HTTPError as e:
            print(f"HTTPエラー: {e.code}")
        except URLError as e:
            print(f"URLエラー: {e.reason}")

    def fetch_merge_request_info(self, merge_request_id):
        project_data = self.get_project_data()
        if project_data:
            repo_url = project_data["web_url"]

        mr_data = self.get_merge_request_data(merge_request_id)
        if mr_data:
            mr_title = mr_data["title"]
            before_hash = mr_data["diff_refs"]["base_sha"]
            after_hash = mr_data["diff_refs"]["head_sha"]

            return repo_url, mr_title, before_hash, after_hash

        return None, None, None, None

if __name__ == "__main__":
    project_id = 38758936
    access_token = "glpat-ZxaZ1xoMhDv5YgswyKsc"
    gitlab_api = GitLabAPI(project_id, access_token)

    from_hash = "9fdfce19"
    to_hash = "0b9a8c18"
    diff_data = gitlab_api.get_diff_data(from_hash, to_hash)
    print(json.dumps(diff_data, indent=2))

    # fetch_files_from_gitlab(from_hash, to_hash, output_zip)を使用して、2つのコミット間の新規ファイルまたは変更されたファイルをダウンロードし、ZIPファイルに保存します。
    output_zip = "output.zip"
    gitlab_api.fetch_files_from_gitlab(from_hash, to_hash, output_zip)

    # get_project_data() を使用して、プロジェクトのデータを取得します。
    project_data = gitlab_api.get_project_data()

    # get_merge_request_data(merge_request_id) を使用して、特定のマージリクエストのデータを取得します。
    merge_request_id = 1
    merge_request_data = gitlab_api.get_merge_request_data(merge_request_id)

    # 定のマージリクエストに関連する情報を取得します。
    merge_request_id = 1
    repo_url, mr_title, before_hash, after_hash = gitlab_api.fetch_merge_request_info(merge_request_id)


#以下の条件でpythonの処理の作成をお願いします。
#- 作成する処理の機能要件
#  - jinja2の初期化を行う処理
#  - フィルターとして以下の処理を登録
#    - 「\n」を「\n    」に置き換える
#    - 入力データに対してconvert_to_date()を実行する
#    - 「\n」やスペースなどの文字列をhtmlのタブなどに変換する
#    - ファイルパスが与えられた場合にパスを削除してファイル名と拡張子に変換
#    - 入力データに対してconvert_to_date()を実行したうえ、時分秒を削除する
#    - 入力データに対してconvert_to_date()を実行したうえ、秒を削除する
#- 作成する処理の非機能要件
#  - 必要であればgitlabAPIを使用すること
#  - 1つの関数は30行までの長さとして処理を分割すること
#  - 日本語のコメントを記載すること
#  - エラー処理を行うこと
#  - PEP8の規定に従うこと

# glpat-ZxaZ1xoMhDv5YgswyKsc
