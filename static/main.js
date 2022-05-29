const Hello = {
    data() {
        return {
            cmd: '',
            cmd_list: [],
            cmd_display: ''
        }
    },
    methods: {
        send_cmd() {
            axios.post('http://192.168.0.20:5000/cmd', { key: this.cmd })
                .then((response) => {
                    this.cmd_list.push(this.cmd)
                    this.cmd_display += this.cmd + '\n'
                    this.cmd = ''
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    },
    mounted() {
        const socket = io.connect();
        socket.on('chats', (msg) => {
            console.log(msg.data)
        })
    }
}

Vue.createApp(Hello).mount('#app')