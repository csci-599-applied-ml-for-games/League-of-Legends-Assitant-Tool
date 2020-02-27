#%%
import os
import os.path
import shutil
def traversefile(workdir):
    for i in range(0,280):
        count = 1
        for file in os.listdir(workdir):
            #拷贝的是文件，如是目录则需要在遍历然后拷贝
            srcFile = os.path.join(workdir,file)
            output_path = 'lol_data_2/training/{}'.format(file.replace('.png',''))
            output_path = output_path.replace('1','')
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            filename = file.replace('item', '{}'.format(i))
            targetFile = os.path.join(output_path, filename)
            shutil.copyfile(srcFile,targetFile)

            count += 1
    return count

traverse = traversefile(workdir='images')
print(traverse)



# %%
def traversefile1(workdir):
    for i in range(280,360):
        count = 1
        for file in os.listdir(workdir):
            #拷贝的是文件，如是目录则需要在遍历然后拷贝
            srcFile = os.path.join(workdir,file)
            output_path = 'lol_data_2/valid/{}'.format(file.replace('.png',''))
            output_path = output_path.replace('1','')
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            filename = file.replace('item', '{}'.format(i))
            targetFile = os.path.join(output_path, filename)
            shutil.copyfile(srcFile,targetFile)

            count += 1
    return count

traverse1 = traversefile1(workdir='images')
print(traverse1)

#%%
import os
import os.path
import shutil
def traversefile1(workdir):
    for i in range(360,400):
        count = 1
        for file in os.listdir(workdir):
            #拷贝的是文件，如是目录则需要在遍历然后拷贝
            srcFile = os.path.join(workdir,file)
            output_path = 'lol_data_2/test/{}'.format(file.replace('.png',''))
            output_path = output_path.replace('1','')
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            filename = file.replace('item', '{}'.format(i))
            targetFile = os.path.join(output_path, filename)
            shutil.copyfile(srcFile,targetFile)

            count += 1
    return count

traverse1 = traversefile1(workdir='images')
print(traverse1)

# %%
