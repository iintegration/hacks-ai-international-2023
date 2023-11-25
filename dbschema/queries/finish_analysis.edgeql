update Lecture
filter .id = <uuid>$lecture_id
set {
    status := <optional str>$status,
    text := <optional str>$text,
    timestamps := <optional json>$timestamps,
    error := <optional str>$error,
    terms := (
        with raw_data := <optional json>$terms,

        for term in json_array_unpack(raw_data) union (
            insert Term {
                term := <str>term['term'],
                definition := <str>term['definition'],
                start_timestamp := <float32>term['start'],
                end_timestamp := <float32>term['end']
            }
        )
    ),
    summary := <optional str>$summary
}