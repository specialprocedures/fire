import mailbox
from email.header import decode_header
import re
from bs4 import BeautifulSoup

act_map = {
    "act": "act",
    "info": "info",
    "infoact": "info",
    "react": "react",
    "inforeact": "info",
}

act_list = ["act", "info", "react"]

encoding_flag = re.compile(r"UTF-8", re.IGNORECASE)


class GmailMboxMessage:
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError("Variable must be type mailbox.mboxMessage")
        else:
            self.email_data = email_data
            self.headers = self.parse_headers()
            self.content = self.get_content()

    def parse_headers(self):
        headers = dict()
        useful_headers = ["reply-to", "date", "subject", "from", "to", "content-type"]
        for header_field in useful_headers:
            header_text = self.decode_mime(self.email_data[header_field])
            headers[header_field.lower()] = header_text

        return headers

    def decode_mime(self, text: str) -> str:
        if isinstance(text, str):
            if encoding_flag.search(text):

                try:
                    return "".join(
                        word.decode(encoding or "utf8")
                        for word, encoding in decode_header(text)
                    )
                except AttributeError:
                    return text

            else:
                return text

    def get_content(self):
        out = []
        for msg_item in self.email_data.walk():
            msg_type = msg_item.get_content_type()
            msg_charset = msg_item.get_content_charset()
            if msg_type == "text/html":
                text = msg_item.get_payload(decode=True).decode(msg_charset)
                return text


# class GmailMboxMessageOld:
#     def __init__(self, email_data):
#         # if not isinstance(email_data, mailbox.mboxMessage):
#         #     raise TypeError("Variable must be type mailbox.mboxMessage")
#         # else:
#         #     self.email_data = email_data

#         # self.act_map = {
#         #     "act": "act",
#         #     "info": "info",
#         #     "infoact": "info",
#         #     "react": "react",
#         #     "inforeact": "info",
#         # }

#         # self.act_list = ["act", "info", "react"]

#         self.parse_headers()

#         if self.headers["subject"]["type"] == "root":

#             self.get_content()
#             self.get_embargo()
#             self.parse_act_type()

#     def parse_headers(self):
#         self.headers = dict()
#         for header_field in self.email_data.keys():
#             if header_field.lower() in (
#                 "date",
#                 "subject",
#                 "from",
#                 "to",
#                 "reply-to",
#                 "cc",
#             ):

#                 header_text = self.decode_mime(self.email_data[header_field])
#                 self.headers[header_field.lower()] = header_text

#         self.headers["subject"] = self.parse_subject(self.headers["subject"])
#         if self.headers.get("reply-to"):
#             self.headers["reply-to"] = self.parse_replyto(self.headers["reply-to"])

#     # def decode_mime(self, text: str) -> str:
#     #     if encoding_flag.search(text):
#     #         return "".join(
#     #             word.decode(encoding or "utf8")
#     #             for word, encoding in decode_header(text)
#     #         )
#     #     else:
#     #         return text

#     def parse_subject(self, text: str) -> dict:

#         if any(i in text.lower()[:3] for i in ("re:", "fwd")):
#             return {
#                 "type": "re/fwd",
#                 "text": text[3:],
#                 "norm_text": self.normalize_text(text[3:]),
#             }

#         else:
#             return {
#                 "type": "root",
#                 "text": text,
#                 "norm_text": self.normalize_text(text),
#             }

#     def parse_replyto(self, text: str):
#         if "<" in text:
#             reply_name, reply_email = [
#                 i.strip().replace(">", "") for i in text.split("<")
#             ]
#         else:
#             reply_name = None
#             reply_email = text

#         reply_root = reply_email.split("@")[0].lower() if reply_email else None

#         return {
#             "reply_name": reply_name,
#             "reply_email": reply_email,
#             "reply_root": reply_root,
#         }

#     def normalize_text(self, x: str):
#         x = re.sub(r"[^A-Za-z0-9 ]+", "", x.lower())
#         return x.strip()

#     def parse_act_type(self):
#         # Get the first token from the cleaned subject
#         text = self.headers["subject"]["norm_text"].split()[0].strip()

#         # If this token is in our list of act_types, set the coresponding value to True
#         if self.act_map.get(text):
#             self.headers["act_type"] = {}

#             act_match = self.act_map[text]
#             if isinstance(act_match, str):
#                 self.headers["act_type"][act_match] = True
#             else:
#                 for act_type in self.act_map[text]:
#                     self.headers["act_type"][act_type] = True

#         # Set other act types to false
#         for act_val in self.act_list:
#             if not self.headers["act_type"].get(act_val):
#                 self.headers["act_type"][act_val] = False

#     def get_content(self):
#         out = []
#         for msg_item in self.email_data.walk():
#             msg_type = msg_item.get_content_type()
#             msg_charset = msg_item.get_content_charset()
#             if msg_type == "text/html":
#                 text = msg_item.get_payload(decode=True).decode(msg_charset)
#                 text = (
#                     BeautifulSoup(text, features="html.parser")
#                     .text.split("**********")[1]
#                     .strip()
#                     .replace("\xa0", "\n")
#                 )
#                 out.append(text)
#         self.headers["content"] = out[0]

#     def get_embargo(self):
#         embargo_sub = "embargo" in (self.headers["subject"]["text"].lower())
#         norm_text = self.headers["content"].lower()
#         embargo_bod = ("embargo" in norm_text) and not (
#             re.match(r"not? ebarg", norm_text)
#         )
#         self.headers["embargo"] = any([embargo_bod, embargo_sub])


# def staff_root(x):
#     if isinstance(x, str):
#         return x.split("@")[0].lower().strip()


# def join_names(x):
#     if isinstance(x, str):
#         split_name = x.split()
#         if len(split_name) == 2:
#             return ".".join(split_name)
#         elif len(split_name) > 2:
#             first_bit = " ".join(split_name[:-1])
#             last_bit = split_name[-1]
#             return ".".join([first_bit, last_bit])
#         else:
#             return x


# def clean_subject(x):
#     x = x.replace("-", " ").strip()
#     for tag in [
#         "act",
#         "info",
#         "infoact",
#         "react",
#         "inforeact",
#         "embargoed",
#         "update",
#         "report",
#     ]:
#         x = re.sub(f"^{tag} ", "", x).strip()
#     return x.strip().replace("  ", " ")


# def clean_timestamp(x):
#     time, date = x.split()
#     time = "/".join([i.zfill(2) for i in time.split("/")])
#     date = ":".join([i.zfill(2) for i in date.split(":")])
#     return f"{time} {date}"
