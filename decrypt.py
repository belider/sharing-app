import base64
import zlib
from google.protobuf.message import DecodeError
from protobuf import versioned_document_pb2, topotext_pb2

def decrypt_note_text(encrypted_base64_text):
    # Декодируем и распаковываем TextDataEncrypted
    data = base64.b64decode(encrypted_base64_text)
    
    if data[0:2] == b'\x1f\x8b':  # Проверка на Gzip
        document_data = zlib.decompress(data, zlib.MAX_WBITS | 16)
    else:
        document_data = zlib.decompress(data)

    try:
        # Декодирование документа с использованием protobuf
        document = versioned_document_pb2.Document()
        document.ParseFromString(document_data)
        
        # Получение последней версии текста
        last_version = document.version[-1]
        text_data = topotext_pb2.String()
        text_data.ParseFromString(last_version.data)
        
        # Возвращаем расшифрованный текст
        # return text_data.string  
        
        # Создание текста с учетом форматирования
        formatted_text = []
        current_position = 0
        task_added = False  # Флаг для предотвращения дублирования символа задачи
        
        for run in text_data.attributeRun:
            # Извлекаем текстовый сегмент, связанный с этим run
            text_chunk = text_data.string[current_position:current_position + run.length]
            current_position += run.length
            
            formatted_segment = text_chunk
            
            # Применение форматирования внутри строки
            if run.fontHints == 1:
                # Если текст заканчивается на перенос строки, добавляем ** перед ним
                if text_chunk.endswith('\n'):
                    formatted_segment = f"**{text_chunk.strip()}**\n"
                else:
                    formatted_segment = f"**{text_chunk.strip()}**"
            
            if run.HasField('paragraphStyle') and run.paragraphStyle.HasField('todo') and not task_added:
                checkbox = '[x]' if run.paragraphStyle.todo.done else '[ ]'
                indent = '    ' * run.paragraphStyle.indent
                # Применяем форматирование только один раз
                formatted_segment = f"{indent}{checkbox} {formatted_segment}"
                task_added = True
            elif run.HasField('paragraphStyle'):
                indent = '    ' * run.paragraphStyle.indent
                formatted_segment = f"{indent}{formatted_segment}"
            
            # Добавляем отформатированный сегмент в результат
            if formatted_segment:
                formatted_text.append(formatted_segment)
            
            # Проверка на конец параграфа или строки
            if text_chunk.endswith('\n'):
                task_added = False  # Сброс флага после завершения параграфа
        
        final_text = "".join(formatted_text)
        return final_text

    except DecodeError as e:
        print(f"Ошибка декодирования Protobuf: {str(e)}")
        return None


## Пример использования decrypt
encrypted_json = {
    "fields": {
        "TitleEncrypted": {
            "value": "0KHRgNC10LTQsCDQv9C70LDQvQ==",
            "type": "ENCRYPTED_BYTES"
        },
        "SnippetEncrypted": {
            "value": "0J7Qv9C40YHQsNGC0YwgMyDQsdC10YLRgSDQvtGCINCY0YDRiyDQsiDQuNC90LHQvtC60YE=",
            "type": "ENCRYPTED_BYTES"
        },
        "TextDataEncrypted": {
            "value": "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",
            "type": "ENCRYPTED_BYTES"
        }
    }
}


note_text = decrypt_note_text(encrypted_json['fields']['TextDataEncrypted']['value'])
print(note_text)