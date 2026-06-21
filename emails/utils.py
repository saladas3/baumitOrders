import os
import email
from email import policy
from email.parser import BytesParser
import imaplib
import quopri
from datetime import datetime
from django.utils import timezone
from django.conf import settings
import re
import base64
from email.header import decode_header, make_header

from .models import Email

class EmailParser:
    @staticmethod
    def decode_header_value(header_value):
        """Decodifică header-ele de email"""
        if not header_value:
            return ""
        try:
            decoded = make_header(decode_header(header_value))
            return str(decoded)
        except:
            return header_value

    @staticmethod
    def parse_date(date_str):
        """Parsează data din email"""
        if not date_str:
            return None
        try:
            # Încearcă mai multe formate de dată
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            try:
                # Fallback pentru formate mai simple
                from email.utils import parsedate
                date_tuple = parsedate(date_str)
                if date_tuple:
                    return datetime(*date_tuple[:6], tzinfo=timezone.utc)
            except:
                pass
        return None

    @staticmethod
    def get_email_body(msg):
        """Extrage body-ul emailului (text și HTML)"""
        body_text = ""
        body_html = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue

                    charset = part.get_content_charset() or 'utf-8'

                    try:
                        decoded_content = payload.decode(charset, errors='ignore')
                    except:
                        decoded_content = payload.decode('utf-8', errors='ignore')

                    if content_type == "text/plain":
                        body_text = decoded_content
                    elif content_type == "text/html":
                        body_html = decoded_content
                except Exception as e:
                    print(f"Error parsing part: {e}")
        else:
            # Email simplu (nu multipart)
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                try:
                    decoded = payload.decode(charset, errors='ignore')
                except:
                    decoded = payload.decode('utf-8', errors='ignore')

                if msg.get_content_type() == "text/html":
                    body_html = decoded
                else:
                    body_text = decoded

        return body_text, body_html

    @staticmethod
    def get_attachments(msg):
        """Extrage atașamentele din email"""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = EmailParser.decode_header_value(filename)
                        payload = part.get_payload(decode=True)
                        if payload:
                            attachments.append({
                                'filename': filename,
                                'content_type': part.get_content_type(),
                                'size': len(payload)
                            })

        return attachments

    @staticmethod
    def parse_email_file(file_path):
        """Parsează un fișier .eml"""
        try:
            with open(file_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)

            # Extrage datele
            subject = EmailParser.decode_header_value(msg.get('Subject', ''))
            sender = EmailParser.decode_header_value(msg.get('From', ''))
            receiver = EmailParser.decode_header_value(msg.get('To', ''))
            message_id = msg.get('Message-ID', '').strip('<>')

            # Parsează datele
            date_sent = EmailParser.parse_date(msg.get('Date', ''))
            date_received = EmailParser.parse_date(msg.get('Received', ''))

            # Extrage body și attachments
            body_text, body_html = EmailParser.get_email_body(msg)
            attachments = EmailParser.get_attachments(msg)

            return {
                'subject': subject,
                'sender': sender,
                'receiver': receiver,
                'date_sent': date_sent,
                'date_received': date_received,
                'body': body_text,
                'body_html': body_html,
                'attachments': attachments,
                'message_id': message_id or os.path.basename(file_path),
                'folder_path': file_path,
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None


class EmailImporter:
    @staticmethod
    def import_from_folder(folder_path, recursive=True):
        """Importă toate emailurile dintr-un folder"""
        imported_count = 0
        skipped_count = 0
        error_count = 0
        errors = []

        # Obține lista fișierelor
        email_files = []
        if recursive:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.eml', '.msg')):
                        email_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.eml', '.msg')):
                    email_files.append(os.path.join(folder_path, file))

        print(f"Found {len(email_files)} email files")

        for file_path in email_files:
            try:
                data = EmailParser.parse_email_file(file_path)
                if not data:
                    error_count += 1
                    errors.append(f"Failed to parse: {file_path}")
                    continue

                # Verifică dacă emailul există deja
                if Email.objects.filter(message_id=data['message_id']).exists():
                    skipped_count += 1
                    continue

                # Salvează în baza de date
                email_obj = Email.objects.create(
                    subject=data['subject'],
                    sender=data['sender'],
                    receiver=data['receiver'],
                    date_sent=data['date_sent'],
                    date_received=data['date_received'],
                    body=data['body'],
                    body_html=data['body_html'],
                    attachments=data['attachments'],
                    message_id=data['message_id'],
                    folder_path=data['folder_path'],
                )
                imported_count += 1

                if imported_count % 100 == 0:
                    print(f"Imported {imported_count} emails...")

            except Exception as e:
                error_count += 1
                errors.append(f"Error importing {file_path}: {str(e)}")

        return {
            'imported': imported_count,
            'skipped': skipped_count,
            'errors': error_count,
            'error_details': errors
        }