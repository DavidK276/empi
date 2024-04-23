// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { User } from '$lib/objects/user';
import type { Participant } from '$lib/objects/participant';

declare global {
    namespace App {
        // interface Error {}
        interface Locals {
            user?: User,
            participant?: Participant
        }
        // interface PageData {
        //     user: User | undefined
        //     attrs: Attribute[] | undefined
        // }
        // interface PageState {}
        // interface Platform {}
    }
}

export {};
