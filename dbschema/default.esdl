module default {
    abstract type User {
        required name: str;
        required is_admin: bool {
            default := false;
        }
    }
}
