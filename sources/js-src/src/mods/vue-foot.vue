<template>
    <footer class="footbar">
		<div class="sidebar-flag" onclick="util.sidebarUtil.toggle()" title="显示/隐藏导航栏">
			<i class="fa fa-angle-right"></i>
		</div>
		<div class="guide-links">
			<span class="guide-last">
				<span v-if="lastShow">
					<a onclick="util.page.last()"><i class="fa fa-caret-left"></i> {{lastText}}</a>
				</span>
			</span>
			<span class="guide-title">&nbsp;</span>
			<span class="guide-next">
				<span v-if="nextShow">
					<a onclick="util.page.next()">{{nextText}} <i class="fa fa-caret-right"></i></a>
				</span>
			</span>
		</div>
	</footer> 
</template>
<script>
export default {
    props:{
        lastShow : {
            type : Boolean,
            default: true
        },
        lastText : {
            type : String
        },
        nextShow : {
            type : Boolean,
            default: true
        },
        nextText : {
            type : String
        }
    }
}
</script>
<style lang="scss">

.footbar{
    position: fixed;
    left:0;
    bottom:0;
    width:100%;
    height: 40px;
    line-height: 40px;
    z-index: 999;
    padding: 0 4rem;
    /*background:#3f5367;*/
    background: #f2f2f2;
    box-shadow: 0 0 2px rgba(0,0,0,0.25);

    .guide-links{
        text-align: center;

        a {
            color: #8a8a8a;
            cursor: pointer;
        }

        .fa-caret-left{
            font-size:25px;
            vertical-align: sub;
            margin-right: 8px;
        }

        .fa-caret-right{
            font-size:25px;
            vertical-align: sub;
            margin-left: 8px;
        }
    }

    .sidebar-flag{
        position: absolute;
        width: 4rem;
        left: 0;
        text-align:  center;
        font-size: 22px;
        cursor:pointer;
        line-height: 38px;
    }

    .guide-last{
        display: inline-block;
        text-align: right;
        width:45%;
    }

    .guide-next{
        display: inline-block;
        text-align: left;
        width:45%;
    }

    .guide-title{
        font-weight:bold;
        position: relative;
        padding-left: 1.5em;
        font-size: 16px;
        display: inline-block;
        width:8%;
        color:#8a8a8a;

        &:after{
            font-family:"iconfont" !important;
            font-size: 18px;
            font-style:normal;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            left:0;
            bottom: 0px;
            position: absolute;
            content: "\e60e";
            width:100%;
        }
    }
}
</style>


