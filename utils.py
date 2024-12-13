import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from requests.adapters import HTTPAdapter, Retry


def fetch_pdf_bytes(
    url: str,
    *,
    max_retries=5
) -> bytes:

    s = requests.Session()
    retries = Retry(
        total=max_retries,
        status_forcelist=[500, 502, 503, 504]
    )
    s.mount('https://', HTTPAdapter(max_retries=retries))

    r = s.get(url)
    r.raise_for_status()

    return r.content


def get_arxiv_url(
    arxiv_id: str,
    *,
    format: str = 'pdf'
) -> str:

    return f'https://arxiv.org/{format}/{arxiv_id}'


def fetch_pdfs(
    arxiv_ids: list[str]
) -> dict[str, bytes]:

    return {
        arxiv_id: fetch_pdf_bytes(
            get_arxiv_url(arxiv_id)
        )
        for arxiv_id in arxiv_ids
    }


def attach_file(
    msg: MIMEMultipart,
    arxiv_id: str,
    contents: bytes,
    format: str
) -> MIMEMultipart:

    filename = f'{arxiv_id}.{format}'

    attachment = MIMEApplication(contents, _subtype=format)
    attachment.add_header(
        'content-disposition',
        'attachment',
        filename=filename
    )
    msg.attach(attachment)

    return msg


def attach_files(
    msg: MIMEMultipart,
    files: dict[str, bytes],
    *,
    format: str = 'pdf'
) -> MIMEMultipart:

    for arxiv_id, contents in files.items():
        attach_file(
            msg,
            arxiv_id,
            contents,
            format
        )

    return msg


def create_email_str(
    email_from: str,
    email_to: str,
    files: dict[str, bytes]
) -> str:

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to

    attach_files(msg, files)

    return msg.as_string()


def send_via_gmail(
    email_from: str,
    email_to: str,
    password: str,
    msg: str,
    *,
    smtp_host: str = 'smtp.gmail.com',
    smtp_port: int = 465
) -> None:

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, msg)


def main(
    email_from: str,
    email_to: str,
    password: str,
    arxiv_ids: list[str]
) -> None:

    files = fetch_pdfs(arxiv_ids)

    email_str = create_email_str(
        email_from,
        email_to,
        files
    )

    send_via_gmail(
        email_from,
        email_to,
        password,
        email_str
    )
