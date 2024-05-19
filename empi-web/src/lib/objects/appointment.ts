export class Appointment {
	id!: number;
	research!: number;
	when!: string;
	capacity!: number;
	free_capacity!: number;
	comment!: string;
	location!: string;
	info_url!: string;

	getWhenLocal(): string {
		const date = new Date(this.when);
		const timezoneOffset = -date.getTimezoneOffset();
		date.setMinutes(date.getMinutes() + timezoneOffset);
		return date.toISOString().slice(0, -1);
	}
}