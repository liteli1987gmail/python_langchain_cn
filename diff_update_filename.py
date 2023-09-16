
# 读取 a_list.txt 文件，并将内容存储在 a_list 中
with open("a_list.txt", "r") as f:
    a_list = f.read().splitlines()

# 读取 b_list.txt 文件，并将内容存储在 b_list 中
with open("b_list.txt", "r") as f1:
    b_list = f1.read().splitlines()


# 使用列表推导式从 b_list 中删除所有在 a_list 中出现的文件路径
filtered_b_list = [path for path in b_list if path not in a_list]

# 将过滤后的 b_list 重新保存到 b_list.txt 文件中，从而覆盖原文件
with open("untracked_files.txt", "w") as f:
    for path in filtered_b_list:
        f.write(f"{path}\n")

# 更新b_list为删减后的需要翻译的别表，由于下次执行的时候，是要在更新后的清单中循环过滤
with open("b_list.txt", "w") as f:
    for path in filtered_b_list:
        f.write(f"{path}\n")

print("Filtered b_list has been saved back to untracked_files.txt.")
