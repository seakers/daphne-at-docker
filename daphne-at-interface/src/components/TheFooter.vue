<template>
    <footer class="is-main-footer">
        <div class="container">
            <div class="has-text-centered">
                <p><strong>Daphne</strong> by <a href="https://www.selva-research.com">SEAK Lab</a>. The source code is licensed
                    <a href="http://opensource.org/licenses/mit-license.php">MIT</a>.</p>
              <div>{{ timestamp }}</div>
            </div>
        </div>
    </footer>
</template>

<script type = "text/javascript">
    export default {
      name: "TheFooter",
      data() {
        return {
          timestamp: ""
        }
      },
      created() {
        setInterval(this.getNow, 3000);
      },
      methods: {
        getNow: function() {
          const today = new Date();
          const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
          const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
          const dateTime = date +' '+ time;
          this.timestamp = dateTime;
        }
      }
    }

</script>

<style scoped>

</style>