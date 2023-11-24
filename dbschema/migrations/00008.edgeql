CREATE MIGRATION m1iwefg2z2dhug67noyj2dijnw5naxod2hksbee5jb3wrymobaarzq
    ONTO m1tbsrf7wtufkb3f3q3ihjuidyaedm6ta6u34n7rpvhfeluclt4xsa
{
  ALTER TYPE default::Lecture {
      CREATE PROPERTY timestamps: std::str;
  };
};
