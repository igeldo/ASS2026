VI→DE README Logger
Skill này làm 2 việc sau mỗi task trong Claude Code:

Dịch input gốc tiếng Việt của user sang tiếng Đức
Tóm tắt những gì Claude đã làm (bằng tiếng Đức)
Append cả hai vào README.md trong project directory


Khi nào chạy skill này
Tự động: Sau mỗi khi Claude hoàn thành một task mà user đã yêu cầu bằng tiếng Việt.
Thủ công: Khi user gõ một trong các lệnh:

/log
/save
/readme
"ghi vào readme"
"lưu lại"


Workflow
Bước 1 — Xác định nội dung cần log
Thu thập từ context hiện tại:

User input gốc (tiếng Việt): câu lệnh / yêu cầu user vừa gõ
Những gì Claude đã làm: danh sách các hành động thực tế (files tạo/sửa, commands chạy, kết quả)

Bước 2 — Dịch sang tiếng Đức
Dịch toàn bộ sang tiếng Đức:

Dịch input tiếng Việt → tiếng Đức (tự nhiên, không phải dịch máy cứng nhắc)
Viết tóm tắt hành động bằng tiếng Đức (ngắn gọn, súc tích, dạng bullet points)

Lưu ý dịch thuật:

Giữ nguyên tên file, path, command, code snippets — không dịch
Thuật ngữ kỹ thuật (SAP, API, npm, git...) giữ nguyên tiếng Anh
Câu văn tự nhiên theo ngữ pháp Đức, không phải Google Translate

Bước 3 — Append vào README.md
Tìm file README.md trong working directory hiện tại. Nếu chưa có, tạo mới.
Append block sau vào cuối file:
markdown---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
[Bản dịch tiếng Đức của user input]

### Durchgeführte Aktionen
- [Hành động 1 bằng tiếng Đức]
- [Hành động 2 bằng tiếng Đức]
- [...]

### Ergebnis
[Kết quả cuối cùng, 1-2 câu tiếng Đức]
Quan trọng:

LUÔN dùng --- để phân tách giữa các session log
KHÔNG thêm timestamp vào header
KHÔNG xóa nội dung cũ — chỉ append
Nếu README đã có nội dung khác (project description, etc.), append xuống dưới cùng

Bước 4 — Xác nhận với user
Sau khi ghi xong, thông báo ngắn gọn bằng tiếng Việt:
✅ Đã ghi vào README.md — [tên file] ([số dòng mới])

Ví dụ thực tế
User input (tiếng Việt):

"tạo file config cho database postgresql, kết nối với port 5432"

Sau khi skill chạy, README.md sẽ có thêm:
markdown---

## Session Log

### Benutzeranfrage (Übersetzt aus dem Vietnamesischen)
Erstelle eine Konfigurationsdatei für eine PostgreSQL-Datenbank mit Verbindung über Port 5432.

### Durchgeführte Aktionen
- `db_config.py` erstellt mit PostgreSQL-Verbindungsparametern
- Standardport 5432 konfiguriert
- Umgebungsvariablen für Datenbankzugangsdaten eingerichtet (`.env`-Vorlage)

### Ergebnis
Datenbankverbindungsdatei erfolgreich erstellt und einsatzbereit.

Edge Cases
Tình huốngXử lýUser input pha trộn tiếng Anh/ViệtDịch phần tiếng Việt, giữ nguyên tiếng AnhREADME.md chưa tồn tạiTạo mới với header mặc định rồi appendTask rất ngắn (1 hành động)Vẫn log, chỉ có 1 bullet point trong AktionenUser gõ /log mà không có task nàoHỏi lại "Bạn muốn log task nào?"Working directory không rõDùng project root hoặc thư mục hiện tại của terminal