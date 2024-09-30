export class Research {
	url?: string;
	id?: number;
	nanoid?: string;
	name!: string;
	comment!: string;
	info_url!: string;
	points!: number
	created!: string
	is_protected!: boolean;
	is_published!: boolean;
	has_open_appointments!: boolean;
	email_recipients?: string;
}