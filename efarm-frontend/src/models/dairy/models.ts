export class Cow {
  id!: number;
  name!: string;
  breed!: string;
  date_of_birth!: string;
  sire!: Cow | null;
  dam!: Cow | null;
  calf!: Cow | null;
  gender!: string;
  availability_status!: string;
  pregnancy_status!: string;
  date_of_death!: string | null;
  tag_number!: string
};