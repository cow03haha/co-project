const Hello = {
    data() {
        return {
            cmd: '',
            cmd_list: []
        }
    },
    methods: {
        async update_chat() {
            const req = await fetch('cmd_list')
            const data = await req.json()
            this.cmd_list = data
        },
        async send_cmd() {
            await fetch('cmd', {
                method: 'post',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({key: this.cmd.toLowerCase()})
            })
            this.cmd = ''
            this.update_chat()
        }
    },
    watch: {
        cmd_list(_new, old) {
            this.$nextTick(() => {
                const chat = this.$refs.input_chat
                chat.scrollTop = chat.scrollHeight
            })
        }
    },
    mounted() {
        this.update_chat()
    }
}

Vue.createApp(Hello).mount('#app')