export class Research {
	url?: string;
	id?: number;
	nanoid?: string;
	name!: string;
	comment!: string;
	info_url: string | undefined;
	points!: number
	created!: string
	is_protected!: boolean;
	is_published!: boolean;
	open_appointment_count!: number;
	available_capacity!: number;
	email_recipients?: string;
}
