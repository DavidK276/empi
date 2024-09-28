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
		if (this.when == null) {
			return "";
		}
		const date = new Date(this.when);
		date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
		return date.toISOString().slice(0, -1);
	}
}