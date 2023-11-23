with result := (insert Lecture {
    file := (insert File {
        filename := <str>$filename
    })
})

select result { id, object_name := <str>(.file.id) }