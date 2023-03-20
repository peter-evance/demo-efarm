export class Cow {
  id!: number;
  name!: string;
  breed!: string;
  date_of_birth!: Date;
  sire!: Cow | null;
  dam!: Cow | null;
  calf!: Cow | null;
  gender!: string;
  availability_status!: string;
  pregnancy_status!: string;
  date_of_death!: string | null;
  tag_number!: string
};



export class Lactation {
  id!: number;
  start_date!: Date; // formatted as YYYY-MM-DD
  end_date?: Date; // formatted as YYYY-MM-DD or null
  cow!: number; // cow ID
  cow_tag_number!: string;
  cow_breed!: string;
  lactation_number!: number;
  pregnancy!: number; // pregnancy ID
  lactation_duration!: string;
  lactation_stage!: string;
  end_date_!: string;
}

export class Milk {
  id!: number;
  cow!: Cow;
  cow_tag_number!: string;
  cow_breed!: string;
  milking_date!: Date; // formatted as YYYY-MM-DD
  amount_in_kgs!: number;
  lactation!: Lactation;
}


export class Pregnancy {
  id!: number;
  cow!: Cow;
  cow_tag_number!: string;
  cow_breed!: string;
  start_date!: Date;
  date_of_calving?: Date | null;
  pregnancy_status!: string;
  pregnancy_notes?: string;
  calving_notes?: string;
  pregnancy_scan_date?: Date | null;
  pregnancy_failed_date?: Date | null;
  pregnancy_outcome!: string | null;
  pregnancy_duration!: string | null;
  due_date!: string | null;
  lactation_stage!: string | null;
}

