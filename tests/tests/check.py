import os

base = r"C:\Users\26647\Desktop\CourseWork\view\assets"
bg_dir = os.path.join(base, "backgrounds")

print("assets 目录下的内容:")
for f in os.listdir(base):
    print("  ", f)

print("\nbackgrounds 目录是否存在:", os.path.exists(bg_dir))
if os.path.exists(bg_dir):
    print("backgrounds 目录内容:")
    for f in os.listdir(bg_dir):
        print("  ", f)
else:
    print("⚠ backgrounds 目录不存在，需要创建！")