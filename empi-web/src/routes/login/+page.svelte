<script lang="ts">
    import {API_ENDPOINT} from '$lib/constants';

    function setCookie(cname: string, cvalue: string, exdays: number, deleteFirst?: boolean) {
        if (deleteFirst === undefined && deleteFirst) {
            document.cookie = `${cname}=; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
        }
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = `${cname}=${cvalue}; ${expires};`;
        console.log("done");
    }

    async function login(e: SubmitEvent) {
        let form = e.target as HTMLFormElement | undefined;
        let formData = new FormData(form, e.submitter)
        let response = await fetch(API_ENDPOINT + "rest-auth/login/", {
            body: formData,
            method: 'POST'
        });
        let text = await response.blob().then(blob => blob.text());
        let responseJSON = JSON.parse(text);
        let key: string = responseJSON.key;
        setCookie("sessionid", key, 7, true);
    }
</script>
<form on:submit|preventDefault={login}>
    <label for="username">Username: </label>
    <input type="text" id="username" name="username" required>
    <label for="password">Password: </label>
    <input type="text" id="password" name="password" required>
    <button type="submit" name="submit">Log in</button>
</form>
