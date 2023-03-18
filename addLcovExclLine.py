import argparse
import datetime
import pathlib
import subprocess
import sys
import re
def get_files(path: pathlib.Path, targets: list[str] = None) -> list[str]:
    """ファイルのパスをリストで返します。

    Args:
        path: gitレポジトリのパス。
        targets:  対象のファイル名。指定されない場合、全てのファイルが対象になります。

    Returns:
        ファイルパスのリスト。
    """
    if targets:
        return [f for f in targets if (path / f).is_file()]
    else:
        cmd = ['git', 'ls-files']
        return subprocess.check_output(cmd, cwd=path, encoding='utf-8').splitlines()

def get_commit_date(path: str, path2: str, commit_hash: str) -> datetime.datetime:
    """指定したコミットの日付を返します。

    Args:
        path: ファイルへのパス。
        commit_hash: コミットのハッシュ値。

    Returns:
        日付をdatetimeオブジェクトとして返します。
    """
    cmd = ['git', 'show', '-s', '--format=%ci', commit_hash, '--', path]
    date_str = subprocess.check_output(cmd, cwd=path2, encoding='utf-8')
    temp = date_str.split()[0]
    return datetime.datetime.fromisoformat(date_str.split()[0])

def get_target_lines(path: pathlib.Path, filename: str, commit_authors: list[str] = None, date_from: datetime.datetime = None,
                     date_to: datetime.datetime = None, commit_hashes: list[str] = None) -> set[int]:
    """除外すべき行番号のセットを返します。

    Args:
        path: gitレポジトリのパス。
        filename: 対象のファイル名。
        commit_authors: 対象のコミット・オーサー。指定されない場合、全てのコミット・オーサーが対象になります。
        date_from: 対象期間の開始日。指定されない場合、全てのコミットが対象となります。
        date_to: 対象期間の終了日。指定されない場合、全てのコミットが対象となります。
        commit_hashes: 対象のコミット・ハッシュ。指定されない場合、全てのコミットが対象となります。

    Returns:
        除外すべき行番号のセット。
    """
    cmd = ['git', 'blame', filename]
    blame_output = subprocess.check_output(cmd, cwd=path, encoding='utf-8')

    target_lines = set()
    for line in blame_output.splitlines():
        author = line.split(' ')[1][1:]
        if commit_authors and author not in commit_authors:
            continue
        commit_hash = line.split(' ')[0][1:]
        if commit_hashes and commit_hash not in commit_hashes:
            continue
        commit_date = get_commit_date(filename, path, commit_hash)
        if (date_from and commit_date < date_from) or (date_to and commit_date > date_to):
            continue
        lineNum = line.split()[5].split(')')[0]

        target_lines.add(int(lineNum) - 1)

    return target_lines

def exclude_lines(path: pathlib.Path, filename: str, target_lines: set[int]) -> None:
    """Exclude the specified lines in the file.

    Args:
        path: Path to the git repository.
        filename: Name of the file to exclude lines.
        target_lines: A set of line numbers to exclude.
    """
    with open(path / filename, 'r') as f:
        lines = f.readlines()

    for i in target_lines:
        lines[i] = lines[i].rstrip() + ' // LCOV_EXCL_LINE\n'

    with open(path / filename, 'w') as f:
        f.writelines(lines)
        
def main() -> None:
    """Main function to exclude lines from files.

    This function parses the command line arguments, and then excludes lines from the files that match the specified
    conditions.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='ファイルから指定の条件に一致する行を除外します。')
    parser.add_argument('path', type=pathlib.Path, help='git リポジトリへのパス')
    parser.add_argument('--targets', type=str, nargs='*', help='対象ファイル名')
    parser.add_argument('--authors', type=str, nargs='*', help='対象コミット作成者')
    parser.add_argument('--from', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), dest='date_from',
                        help='対象期間の先頭日時（YYYY-MM-DD を指定）')
    parser.add_argument('--to', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), dest='date_to',
                        help='対象期間の末尾日時（YYYY-MM-DD を指定）')
    parser.add_argument('--hashes', type=str, nargs='*', default=[], help='ハッシュ値')
    args = parser.parse_args()

    if not any([args.path, args.targets, args.authors, args.date_from, args.date_to, args.hashes]):
        parser.print_usage()
        sys.exit(1)

    files = get_files(args.path, args.targets)

    for file in files:
        target_lines = get_target_lines(args.path, file, args.authors, args.date_from, args.date_to, args.hashes)
        exclude_lines(args.path, file, target_lines)
        print(f'{file} から {len(target_lines)} 行を除外しました。')

if __name__ == '__main__':
    main()
