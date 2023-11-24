update Lecture
filter .id = <uuid>$lecture_id
set {
    status := <optional str>$status,
    text := <optional str>$text,
    error := <optional str>$error
}