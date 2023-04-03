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
  date_of_death?: Date | null;
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
  end_date_!: string; // Still not fully formatted since the back end sometimes returns "Ended"
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

export class Inseminator {
  id!: number;
  name!: string;
  company?: string | null;
  license_number!: string;
  phone_number?: string | null;
  email!: string;
  address?: string | null;
  notes?: string | null;
}

export class Semen {
  id?: number;
  inseminator!: Inseminator;
  producer!: string;
  semen_batch!: string;
  date_of_production!: Date; // formatted as YYYY-MM-DD
  date_of_expiry!: Date; // formatted as YYYY-MM-DD
  notes?: string | null;
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


export class Insemination {
  date_of_insemination!: Date; 
  cow!: Cow;
  pregnancy!: Pregnancy | null;
  success?: boolean;
  notes?: string;
  inseminator?: Inseminator;
  semen?: Semen;
  days_since_insemination!: string;
}

