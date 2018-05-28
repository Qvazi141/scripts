import os
import re
import zipfile

# Enter your path
PATH = r"/home/eugenebulakhau/PycharmProjects/orginize_dir/test"
# Enter path for archive
PATH_FOR_ARCHIVE = r"/home/eugenebulakhau/PycharmProjects/orginize_dir/test"


# функция для поиска всех файловв которые удовлетворяют шаблону
def search_file_for_archive(listdir):
    result = []
    for file in listdir:
        if os.path.isfile(PATH + '/' + file) and re.match(r".*(\d{4}_\d\d_\d\d).*", file):
            result.append(file)
    return result


# функция для архивации списка файлов
def archiving_files(files_for_archive):
    try:
        with zipfile.ZipFile("{0}/{1}.zip".format(PATH_FOR_ARCHIVE, files_for_archive[0]), 'w') as myzip:
            for file in files_for_archive[1:]:
                myzip.write(os.path.join(PATH, file), arcname=file)
    except zipfile.BadZipFile:
        print("Something is wrong with the archive")
    except zipfile.LargeZipFile:
        print("Something is wrong with the archive")
    except FileExistsError:
        print("File does not exist")


# фунция удаления заархвированных файлов
def deleting_archived_files(files_for_archive):
    try:
        for file in files_for_archive[1:]:
            os.remove(os.path.join(PATH, file))
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission denied")


if __name__ == "__main__":
    all_files = os.listdir(PATH)
    files = search_file_for_archive(all_files)
    del all_files
    archive = []
    while files:
        match = re.search(r"\d{4}_\d\d_\d\d", files[0])
        archive.append(match[0])
        for file in files:
            if re.search(r"\d{4}_\d\d_\d\d", file)[0] == match[0]:
                archive.append(file)
        archiving_files(archive)
        deleting_archived_files(archive)
        files = [x for x in files if x not in archive]  # удаляем из списка, то что уже заархивировали
        archive = []
