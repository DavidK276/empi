import type { Research } from '$lib/objects/research';
import type { Participant } from '$lib/objects/participant';

export class Participation {
	id!: number;
	appointment?: number;
	research!: Research;
	participant!: Participant;
	is_confirmed!: boolean;
	token?: string;
}