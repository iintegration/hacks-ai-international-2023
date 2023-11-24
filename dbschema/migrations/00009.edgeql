CREATE MIGRATION m1y34hnzojd6v53fa77zyq7xfju5pxlgywpag62n6s4oxjjyq5tdkq
    ONTO m1iwefg2z2dhug67noyj2dijnw5naxod2hksbee5jb3wrymobaarzq
{
  ALTER TYPE default::Lecture {
      ALTER PROPERTY timestamps {
          SET TYPE std::json USING (<std::json>.timestamps);
      };
  };
};
