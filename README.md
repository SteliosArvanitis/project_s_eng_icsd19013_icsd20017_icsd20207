# Εργασία Τεχνολογίας Λογισμικού 2024
---
Αυτό το repository εμπεριέχει την απαλλακτική εργασία των φοιτητών
##### Αρβανίτης Στυλιανός 321/2019013
##### Δημήτρης Αρβανιτης 321/2020017
##### Ιωάννα Σπαχίου 321/2020207
---
### Οδηγίες Εγκατάστασης
Τα προαπαιτούμενα προγράμματα για την επιτυχή εκκίνηση της εργασίας μας είναι:
<br />-Python 3
<br />-Visual studio code
<br />-XAMPP

---

### Βήματα εκτέλεσης <br />
1. Εκτέλεση της εφαρμογής XAMPP
2. Χρησιμοποιούμε τα κατάλληλα πλήκτρα για να εκκηνίσουμε **Apache** και **MySQL**<br />
![εικόνα](https://github.com/user-attachments/assets/59024810-6783-4237-8675-bc303076a15c)
3. Πιέζουμε το πλήκτρο **Admin** δίπλα απο το MySQL το οποίο θα μας ανοίξει την σελίδα διαχείρησης των βάσεων δεδομένων μας
4. Δημιουργούμε μια νέα βάση δεδομένων με όνομα `dbarv`
5. Ανοίγουμε τον φάκελο του project file με visual stydio code
6. Μέσα στην εφαρμογή πατάμε το Terminal->New Terminal<br />
![εικόνα](https://github.com/user-attachments/assets/c851692c-2bb7-4365-bb7f-b1e1b1755c49)
7. Στο Terminal που εμφανίστηκε στο κάτω μέρος της εμαρμογής εκτελούμε την εντολή <br />
`pip install -r requirements.txt`<br /> το οποίο μας εγκαθιστά τις απαραίτητες βιβλιοθήκες
8. Αφού ολοκληρωθεί η λήψη των απαιτούμενων βιβλιοθηκών εκτελούμε την εντολή <br /> `uvicorn app.main:app --port 9000 --reload`, για την εκκίνηση του server που υλοποιεί το rest api μας
9. **Η εφαρμογή είναι έτοιμη για να δεχτεί αιτήματα!**

---
### Documentation εφαρμογής<br />
Μετά την εκκίνηση του Server σε κάποιον browser πληκτρολογούμε `127.0.0.1:9000/docs` για να εμφανιστεί το documentation του api μας.

---

### Αποτελέσματα Testing <br />
Για τη φάση του testing χρησιμοποιήσαμε το **Insomnia Client**.<br />
Τα requests που κάναμε βρίσκονται στο αρχείο `icsd19013_icsd20017_icsd20207_testing_results_for_insomnia.json` το οποίο μπορεί να γίνει απευθείας import στο Insomnia για να εμφανιστούν τα requests που χρησιμοποιήσαμε.

