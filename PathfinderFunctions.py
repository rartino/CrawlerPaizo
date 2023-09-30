import zipfile
import io, os
from bs4 import BeautifulSoup


def soup_function(value_holder):
    page_data = value_holder.text
    inner_soup = BeautifulSoup(page_data, features="html.parser")
    return inner_soup


def format_book_title(title_with_tag):
    title_with_tag = title_with_tag.find('b').text
    title_with_tag = title_with_tag.replace('<b>', '')
    title_with_tag = title_with_tag.replace('</b>', '')
    title_with_tag = title_with_tag.replace(':', '')
    return title_with_tag


def unzip_file(content):
    unzip = zipfile.ZipFile(io.BytesIO(content))
    return unzip


def set_unzip_folder(zipbytes, outdir):
    zipbytes.extractall(outdir)


def change_crawler_session(login_path, user_credentials, account_files, current_session):
    current_session.get(login_path)
    current_session.post(login_path, user_credentials)
    return current_session.get(account_files)


def get_file(link_to_file, exts, current_session, book_name):
    link = link_to_file.get('href')
    outdir = './PaizoLibrary/{}'.format(book_name)
    if link is not None and any(link.endswith(ext) for ext in exts):
        print("Found valid download link, downloading:",book_name)
        response = current_session.get(link_to_file.get('href'))
        if link.endswith(".zip"):
            zip_bin = unzip_file(response.content)
            set_unzip_folder(zip_bin, outdir)
        else:
            filename = link.rpartition("/")[2]
            os.mkdir(outdir)
            with open(os.path.join(outdir,filename), "wb") as f:
                f.write(io.BytesIO(response.content).getbuffer())
        return True
    return False

