with result := (insert Lecture {
    file := (insert File {
        filename := <str>$filename,
        filename_suffix := <str>$filename_suffix
    })
})

select result { id, object_name := .file.object_name }