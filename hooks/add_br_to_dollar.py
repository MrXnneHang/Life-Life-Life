import sys
import re

def main():
    # 获取需要检查的文件列表
    # pre-commit 钩子会将文件名作为命令行参数传递
    files_to_check = sys.argv[1:]

    modified_files = []

    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            file_modified = False
            for line in lines:
                # 检查行是否以 $ 结尾，并且 $ 前面不是反斜杠（避免匹配转义的 $）
                # 注意：这里的 $ 必须是行的最后一个字符
                if re.search(r'(?<!\\)\$$', line):
                    new_line = line.rstrip('\n') + '<br>\n' # 在 $ 后添加 <br>，并保留原始换行符
                    new_lines.append(new_line)
                    file_modified = True
                else:
                    new_lines.append(line)

            if file_modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                modified_files.append(filepath)

        except Exception as e:
            print(f"处理文件 '{filepath}' 时出错: {e}", file=sys.stderr)
            sys.exit(1) # 如果出错，退出状态码非零

    if modified_files:
        print("以下文件已修改并重新暂存（在 '$' 后添加了 '<br>'）：")
        for f in modified_files:
            print(f"- {f}")
        # pre-commit 会自动重新暂存被脚本修改的文件，不需要手动 git add
        # 但为了确保 commit 包含这些更改，需要让 pre-commit 知道有文件被修改
        # 抛出异常或返回非零状态码会让 pre-commit 暂停 commit，但这里我们希望它继续
        # pre-commit 的默认行为是如果文件内容改变，会自动 git add 并重新运行钩子
        # 所以通常情况下，只要文件被修改，pre-commit 就会处理
        sys.exit(0) # 成功完成，退出状态码为 0
    else:
        print("没有找到需要修改的文件。")
        sys.exit(0)

if __name__ == '__main__':
    main()