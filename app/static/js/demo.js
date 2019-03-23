

 function notifyMsg(msg){
       var notify =  $.notify({
            icon: 'la la-bell',
            title: '警告',
            message: flash_info[0],
        },{
            type: 'warning',
            placement: {
                from: "bottom",
                align: "right"
            },
            time: 1000,
        });

       return notify;
    }
for (a_flash_info in flash_info){
    notifyMsg(a_flash_info)
}
//$.notify({
//	icon: 'la la-bell',
//	title: '错误',
//	message: flash_info[0],
//},{
//	type: 'success',
//	placement: {
//		from: "bottom",
//		align: "right"
//	},
//	time: 1000,
//});
