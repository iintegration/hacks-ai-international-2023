CREATE MIGRATION m1mhde2r5vzvr4i4qk3nu4mjdwgklwo3qv7yyf2tcmevsokwaahicq
    ONTO m1y34hnzojd6v53fa77zyq7xfju5pxlgywpag62n6s4oxjjyq5tdkq
{
  ALTER TYPE default::File {
      CREATE REQUIRED PROPERTY filename_suffix: std::str {
          SET REQUIRED USING ('.mp3');
          CREATE ANNOTATION std::description := 'Расширение файла пользователя';
      };
      CREATE PROPERTY object_name := ((<std::str>.id ++ .filename_suffix));
  };
};
