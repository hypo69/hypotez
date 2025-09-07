<!-- wp:paragraph -->
<p>בכל פעם שאתם מצלמים תמונה, המצלמה שלכם רושמת לקובץ לא רק את התמונה עצמה, אלא גם מידע שירות: דגם המצלמה והעדשה, תאריך ושעת הצילום, מהירות תריס, צמצם, ISO, קואורדינטות GPS. נתונים אלו נקראים **EXIF (Exchangeable Image File Format)**.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>אף של-PowerShell יש כלים מובנים לקריאת חלק מהמטא-נתונים, הם מוגבלים. כדי לגשת ל**כל** המידע, נדרש כלי מיוחד. במאמר זה אשתמש ב-**ExifTool**.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>**ExifTool** הוא כלי עזר חינמי, חוצה פלטפורמות, בקוד פתוח, שנכתב על ידי פיל הארווי. הוא נחשב לסטנדרט הזהב לקריאה, כתיבה ועריכה של מטא-נתונים במגוון רחב של פורמטים (תמונות, אודיו, וידאו, PDF ועוד). ExifTool מכיר אלפי תגים ממאות יצרני מכשירים, מה שהופך אותו לכלי המקיף ביותר בקטגוריה שלו.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">הורדה והגדרה נכונה</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>לפני כתיבת קוד כלשהו, יש להכין את כלי העזר עצמו.</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list"><!-- wp:list-item -->
<li>היכנסו ל**אתר הרשמי של ExifTool: <a href="https://exiftool.org/">https://exiftool.org/</a>**. בעמוד הראשי, מצאו והורידו את **"Windows Executable"**.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong>שינוי שם (שלב קריטי!):</strong> הקובץ שהורדתם ייקרא <code>exiftool(-k).exe</code>. זו לא מקריות. שנו את שמו ל-**<code>exiftool.exe</code>**, כדי **לבטל את מצב ה"השהיה"**, המיועד למשתמשים המפעילים את התוכנה בלחיצה כפולה.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong>אחסון:</strong> יש לכם שתי אפשרויות עיקריות היכן לאחסן את <code>exiftool.exe</code>.<!-- wp:list -->
<ul class="wp-block-list"><!-- wp:list-item -->
<li><strong>אפשרות 1 (פשוטה): באותה תיקיה כמו הסקריפט שלכם.</strong> זו הדרך הקלה ביותר. סקריפט ה-PowerShell שלכם תמיד יוכל למצוא את כלי העזר, מכיוון שהוא נמצא בסמוך. אידיאלי לסקריפטים ניידים שאתם מעבירים ממחשב למחשב.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong>אפשרות 2 (מומלצת לשימוש תכוף): בתיקיה מתוך משתנה המערכת <code>PATH</code>.</strong> משתנה <code>PATH</code> הוא רשימת ספריות שבהן Windows ו-PowerShell מחפשים אוטומטית קבצי הפעלה.<br>אתם יכולים ליצור תיקיה (לדוגמה, <code>C:\Tools</code>), לשים בה את <code>exiftool.exe</code> ולהוסיף את <code>C:\Tools</code> למשתנה המערכת <code>PATH</code>.<br>לאחר מכן תוכלו להפעיל את <code>exiftool.exe</code> מכל תיקיה בכל קונסולה.</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></li>
<!-- /wp:list-item --></ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>סקריפטים להוספה ל-<code>$PATH</code>:<br>הוספת ספרייה ל-<code>PATH</code> עבור המשתמש הנוכחי<br>הוספת ספרייה ל-<code>PATH</code> המערכתי עבור כל המשתמשים</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading -->
<h2 class="wp-block-heading">PowerShell ותוכניות חיצוניות</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>כדי להשתמש ב-ExifTool ביעילות, יש לדעת כיצד PowerShell מפעיל קבצי <code>.exe</code> חיצוניים.<br>הדרך הנכונה והאמינה ביותר להפעלת תוכניות חיצוניות היא **אופרטור הקריאה <code>&amp;</code> (אמפרסנד)**.<br>PowerShell יחזיר שגיאה במקרה שנתיב התוכנית מכיל רווחים. לדוגמה, <code>C:\My Tools\exiftool.exe</code>.<br><code>&amp;</code> (אמפרסנד) אומר ל-PowerShell: "הטקסט שאחרי בגרשיים, – זהו הנתיב לקובץ ההפעלה. הפעל אותו, וכל מה שאחריו, – אלו הארגומנטים שלו".</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code># תחביר נכון
&amp;amp; "C:\Path With Spaces\program.exe" "argument 1" "argument 2"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>תמיד השתמשו ב-<code>&amp;</code>, כאשר אתם עובדים עם נתיבים לתוכניות במשתנים או נתיבים שעשויים להכיל רווחים.</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading -->
<h2 class="wp-block-heading">טריקים מעשיים: ExifTool + PowerShell</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>כעת נשלב את הידע שלנו.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 1: חילוץ בסיסי וצפייה אינטראקטיבית</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>הדרך הפשוטה ביותר לקבל את כל הנתונים מתמונה ולבחון אותם – היא לבקש אותם בפורמט JSON ולהעביר אותם ל-<code>Out-ConsoleGridView</code>.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$photoPath = "D:\Photos\IMG_1234.JPG"

# 1. מפעילים את exiftool עם המתג -json לפלט מובנה
# 2. ממירים את טקסט ה-JSON לאובייקט PowerShell
#    מפעילים את exiftool.exe ישירות, ללא משתנה ואופרטור קריאה &amp;amp;.
$exifObject = exiftool.exe -json $photoPath | ConvertFrom-Json

# 3. הופכים את האובייקט ה"רחב" לטבלת "פרמטר-ערך" נוחה
$reportData = $exifObject.psobject.Properties | Select-Object Name, Value

# 4. מציגים את התוצאה בחלון אינטראקטיבי לניתוח
$reportData | Out-ConsoleGridView -Title "מטא-נתונים של קובץ: $($photoPath | Split-Path -Leaf)"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>קוד זה יפתח חלון אינטראקטיבי שבו תוכלו למיין נתונים לפי שם פרמטר או ערך, ולסנן אותם, פשוט על ידי התחלת הקלדת טקסט. זה נוח להפליא למציאת מידע נחוץ במהירות.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 2: יצירת דוח נקי ושליחה ל"התקנים" שונים</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><code>Out-ConsoleGridView</code> – זו רק ההתחלה. אתם יכולים להפנות נתונים מעובדים לכל מקום, באמצעות פקודות <code>Out-*</code> אחרות.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>נניח שיש לנו נתונים במשתנה <code>$reportData</code> מהדוגמה הקודמת.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">**א) שליחה לקובץ CSV עבור Excel**</h4>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$reportData | Export-Csv -Path "C:\Reports\photo_exif.csv" -NoTypeInformation -Encoding UTF8
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>הפקודה <code>Export-Csv</code> יוצרת קובץ מובנה באופן מושלם שניתן לפתוח ב-Excel או ב-Google Sheets.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">**ב) שליחה לקובץ טקסט**</h4>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code># לעיצוב יפה, השתמשו תחילה ב-Format-Table
$reportData | Format-Table -AutoSize | Out-File -FilePath "C:\Reports\photo_exif.txt"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>הפקודה <code>Out-File</code> תשמור לקובץ עותק טקסט מדויק של מה שאתם רואים בקונסולה.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":4} -->
<h4 class="wp-block-heading">**ג) שליחה ללוח הגזירים**</h4>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>רוצים להדביק נתונים במהירות למייל או לצ'אט? השתמשו ב-<code>Out-Clipboard</code>.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$reportData | Format-Table -AutoSize | Out-String | Out-Clipboard
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>כעת תוכלו ללחוץ <code>Ctrl+V</code> בכל עורך טקסט ולהדביק טבלה מעוצבת בקפידה.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 3: קבלת נתונים ספציפיים לשימוש בסקריפט</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>לעתים קרובות אינכם זקוקים לכל הדוח, אלא רק לערך אחד או שניים. מכיוון ש-<code>$exifObject</code> – זהו אובייקט PowerShell רגיל, תוכלו לגשת בקלות למאפייניו.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code>

$photoPath = "D:\Photos\IMG_1234.JPG"

# מפעילים את exiftool.exe ישירות לפי שם.
# PowerShell ימצא אותו אוטומטית באחת מהתיקיות, המפורטות ב-PATH.
$exifObject = exiftool.exe -json $photoPath | ConvertFrom-Json

# 1. יוצרים אובייקט PowerShell אחד עם שמות מאפיינים מובנים.
#    זה דומה ליצירת רשומה מובנית.
$reportObject = &#91;PSCustomObject]@{ 
    "מצלמה"           = $exifObject.Model
    "תאריך צילום"      = $exifObject.DateTimeOriginal
    "רגישות" = $exifObject.ISO
    "שם קובץ"        = $exifObject.FileName # נוסיף את שם הקובץ להקשר
}

# 2. מציגים את האובייקט הזה בחלון אינטראקטיבי.
#    Out-GridView תיצור אוטומטית עמודות משמות המאפיינים.
$reportObject | Out-ConsoleGridView -Title "מטא-נתונים של קובץ: $(Split-Path $photoPath -Leaf)"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>גישה זו היא הבסיס לכל אוטומציה רצינית, כגון שינוי שמות קבצים על בסיס תאריך הצילום, מיון תמונות לפי דגם מצלמה או הוספת סימני מים עם מידע על חשיפה.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 4: חילוץ אצווה של מטא-נתונים מתיקיה</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>לפעמים צריך לנתח לא תמונה אחת, אלא תיקיה שלמה עם תמונות.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code># מציינים רק את תיקיית התמונות.
$photoFolder = "D:\Photos"

# מפעילים את exiftool.exe ישירות. משתנה לנתיב ואופרטור &amp;amp; אינם נחוצים.
$allExif = exiftool.exe -json "$photoFolder\*.jpg" | ConvertFrom-Json

# הופכים לתצוגה נוחה 
$report = foreach ($photo in $allExif) {
    &#91;PSCustomObject]@{
        # --- נתונים בסיסיים על הקובץ והמצלמה ---
        FileName       = $photo.FileName
        DateTime       = $photo.DateTimeOriginal
        CameraMake     = $photo.Make                 # יצרן (לדוגמה, "Canon", "SONY")
        CameraModel    = $photo.Model                 # דגם מצלמה (לדוגמה, "EOS R5")
        LensModel      = $photo.LensID                # שם מלא של דגם העדשה

        # --- פרמטרי צילום (חשיפה) ---
        ISO            = $photo.ISO
        ShutterSpeed   = $photo.ShutterSpeed
        Aperture       = $photo.Aperture
        FocalLength    = $photo.FocalLength           # אורך מוקד (לדוגמה, "50.0 mm")
        ExposureMode   = $photo.ExposureProgram       # מצב צילום (לדוגמה, "Manual", "Aperture Priority")
        Flash          = $photo.Flash                 # מידע האם הפלאש הופעל

        # --- GPS ונתוני תמונה ---
        GPSPosition    = $photo.GPSPosition           # קואורדינטות GPS כמחרוזת אחת (אם קיימות)
        Dimensions     = "$($photo.ImageWidth)x$($photo.ImageHeight)" # מימדי תמונה בפיקסלים
    }
}

# מציגים נתונים בטבלה אינטראקטיבית בקונסולה
$report | Out-ConsoleGridView -Title "דוח סיכום לתיקיה: $photoFolder"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>💡 אתם מקבלים טבלה מסודרת לכל התיקיה בבת אחת.</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 5: חיפוש רקורסיבי בתיקיות משנה</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>ExifTool יודע לחפש קבצים בכל תיקיות המשנה בעצמו בעת שימוש במתג <code>-r</code>.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code>&amp;amp; $exifToolPath -r -json "D:\Photos" | ConvertFrom-Json |
    Select-Object FileName, Model, DateTimeOriginal |
    Export-Csv "C:\Reports\all_photos_recursive.csv" -NoTypeInformation -Encoding UTF8
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 6: שינוי שמות קבצים לפי תאריך צילום</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>זהו אחד מתרחישי האוטומציה הפופולריים ביותר – קבצים מקבלים שמות לפי תאריך/שעת הצילום.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$exifToolPath = "C:\Tools\exiftool.exe"
$photoFolder = "D:\Photos"

# נשנה שם לפורמט YYYY-MM-DD_HH-MM-SS.jpg
&amp;amp; $exifToolPath -r -d "%Y-%m-%d_%H-%M-%S.%%e" "-FileName&amp;lt;DateTimeOriginal" $photoFolder
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>💡 *ExifTool יכניס אוטומטית את סיומת הקובץ המקורית באמצעות <code>%%e</code>.*</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 7: חילוץ קואורדינטות GPS בלבד</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>שימושי אם אתם רוצים לבנות מפה מהתמונות שלכם.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code># 1. ציינו את הנתיב לתיקיה עם התמונות שלכם
$photoFolder = "E:\DCIM\Camera"

# 2. מפרטים את התגים שאנו צריכים: שם קובץ ושלושה תגי GPS.
#    זה הופך את השאילתה למהירה הרבה יותר מאשר אם היינו מאחזרים את כל התגים.
$tagsToExtract = @(
    "-SourceFile", # SourceFile עדיף על FileName, מכיוון שהוא בדרך כלל מכיל את הנתיב המלא
    "-GPSLatitude",
    "-GPSLongitude",
    "-GPSAltitude"
)

# 3. מפעילים את exiftool.exe ישירות (מכיוון שהוא ב-PATH).
#    המתג -r מחפש קבצים בכל תיקיות המשנה.
#    התוצאה מומרת מיד מ-JSON.
$allExifData = exiftool.exe -r -json $tagsToExtract $photoFolder | ConvertFrom-Json

# 4. מסננים את התוצאות: משאירים רק את האובייקטים שיש להם קו רוחב וקו אורך.
$filesWithGps = $allExifData | Where-Object { $_.GPSLatitude -and $_.GPSLongitude }

# 5. בודקים אם בכלל נמצאו קבצים עם נתוני GPS
if ($filesWithGps) {
    # 6. יוצרים דוח יפה מהנתונים המסוננים.
    #    משתמשים ב-Select-Object לשינוי שמות עמודות ועיצוב.
    $report = $filesWithGps | Select-Object @{Name="שם קובץ"; Expression={Split-Path $_.SourceFile -Leaf}},
                                             @{Name="קו רוחב"; Expression={$_.GPSLatitude}},
                                             @{Name="קו אורך"; Expression={$_.GPSLongitude}},
                                             @{Name="גובה"; Expression={if ($_.GPSAltitude) { "$($_.GPSAltitude) מ" } else { "N/A" }}}

    # 7. מציגים את הדוח הסופי בטבלה אינטראקטיבית בקונסולה.
    $report | Out-ConsoleGridView -Title "קבצים עם נתוני GPS בתיקיה: $photoFolder"

} else {
    # אם לא נמצא דבר, מודיעים על כך בנימוס.
    Write-Host "קבצים עם נתוני GPS בתיקיה '$photoFolder' לא נמצאו." -ForegroundColor Yellow
}
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 8: מחיקה המונית של כל נתוני GPS (לצורך פרטיות)</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code># נמחק את כל תגי ה-GPS מקבצי JPG ו-PNG
&amp;amp; $exifToolPath -r -overwrite_original -gps:all= "D:\Photos"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p>💡 *פעולה זו בלתי הפיכה, לכן גבו את הקבצים לפני הביצוע.*</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 9: המרת זמן צילום לזמן מקומי</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>לפעמים תמונות צולמו באזור זמן אחר. ExifTool יכול להזיז את התאריך.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code># מזיזים את הזמן ב-3 שעות
&amp;amp; $exifToolPath "-AllDates+=3:0:0" "D:\Photos\IMG_*.JPG"
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 10: קבלת רשימה של כל דגמי המצלמות הייחודיים בתיקיה</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$models = &amp;amp; $exifToolPath -r -Model -s3 "D:\Photos" | Sort-Object -Unique
$models | ForEach-Object { Write-Host "דגם: $_" }
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 11: הצגת תגים נחוצים בלבד בפורמט טבלאי</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>&amp;amp; $exifToolPath -T -Model -DateTimeOriginal -ISO -Aperture -ShutterSpeed "D:\Photos\IMG_1234.JPG"
</code></pre>
<!-- /wp:code -->

<!-- wp:paragraph -->
<p><code>-T</code> מציג פלט בפורמט טבלאי, מופרד בטאבים – נוח לעיבוד נוסף.</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 12: בדיקת נוכחות GPS במערך גדול של קבצים</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$files = &amp;amp; $exifToolPath -r -if "$gpslatitude" -p '$FileName' "D:\Photos"
Write-Host "קבצים עם GPS:"
$files
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 13: העתקת מטא-נתונים מקובץ אחד לאחר</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code># 1. בוחרים קובץ ייחוס
$sourceFile = Get-ChildItem "D:\Photos" -Filter "*.jpg" | Out-ConsoleGridView -Title "בחרו קובץ ייחוס"

# 2. אם קובץ ייחוס נבחר, בוחרים קבצי יעד
if ($sourceFile) {
    $targetFiles = Get-ChildItem "D:\Photos\New" -Filter "*.jpg" | Out-ConsoleGridView -Title "בחרו קבצי יעד להעתקת מטא-נתונים" -OutputMode Multiple

    # 3. אם קבצי יעד נבחרו, מבצעים את ההעתקה
    if ($targetFiles) {
        &amp;amp; exiftool.exe -TagsFromFile $sourceFile.FullName ($targetFiles.FullName)
        Write-Host "מטא-נתונים הועתקו מ-$($sourceFile.Name) ל-$($targetFiles.Count) קבצים."
    }
}
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 14: שמירת מטא-נתונים מקוריים לקובץ JSON נפרד לפני שינוי</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$backupPath = "C:\Reports\metadata_backup.json"
&amp;amp; $exifToolPath -r -json "D:\Photos" | Out-File -Encoding UTF8 $backupPath
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה מס' 15: שימוש ב-PowerShell למיון אוטומטי של תמונות לפי תאריך</h3>
<!-- /wp:heading -->

<!-- wp:code -->
<pre class="wp-block-code"><code>$photos = Get-ChildItem "D:\Photos" -Filter *.jpg -Recurse
foreach ($photo in $photos) {
    $meta = &amp;amp; $exifToolPath -json $photo.FullName | ConvertFrom-Json
    $date = Get-Date $meta.DateTimeOriginal -ErrorAction SilentlyContinue
    if ($date) {
        $targetFolder = "D:\Sorted\{0:yyyy}\{0:MM}" -f $date
        if (-not (Test-Path $targetFolder)) { New-Item -Path $targetFolder -ItemType Directory }
        Move-Item $photo.FullName -Destination $targetFolder
    }
}
</code></pre>
<!-- /wp:code -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">דוגמה 16: מציאת כל דגמי המצלמות הייחודיים באוסף</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>אף שניתן לעשות זאת בשורה אחת, הצגה ב-<code>GridView</code> מאפשרת להעתיק מיד את שם הדגם הרצוי.</p>
<!-- /wp:paragraph -->

<!-- wp:code -->
<pre class="wp-block-code"><code># המתג -s3 מציג רק ערכים, -Model - את שם התג
$uniqueModels = &amp;amp; exiftool.exe -r -Model -s3 "D:\Photos" | Sort-Object -Unique

# מציגים ב-GridView לצפייה והעתקה נוחות
$uniqueModels | Out-ConsoleGridView -Title "דגמי מצלמות ייחודיים באוסף"
</code></pre>
<!-- /wp:code -->