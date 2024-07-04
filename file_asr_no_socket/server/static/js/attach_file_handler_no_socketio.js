/* 참고문서
    1. https://purecho.tistory.com/68
    2. https://codepen.io/green526/embed/qBjZLex?height=537&default-tab=html%2Cresult&slug-hash=qBjZLex&editable=true&user=green526&ke-size=size16&name=cp_embed_1
*/

var FILE_NUM = 0; // 첨부된 파일 개수
var FILE_ARRAY = new Array(); // 첨부 파일 저장용 배열

function addFile(obj){
    let max_file_count = 1; // 첨부팡리 최대 개수
    let attach_file_count =  $('.filebox').length; // 현재 첨부된 파일 개수 / $: jQuery를 사용하여 class 잡음
    let remain_file_count = max_file_count - attach_file_count;
    let current_file_count = obj.files.length; // 현재 첨부된 파일 개수
    $('#attached-file-list').attr('hidden', false)
    // 첨부파일 개수 확인
    if (current_file_count > remain_file_count){
        alert(`첨부 파일은 최대 ${max_file_count}개 까지 첨부 가능합니다.`)
    } else{
        for(const file of obj.files){
            // 파일이 음성 파일인지 검증
            if (validation(file)){
                // 파일을 배열에 담기
                let reader = new FileReader();
                reader.readAsDataURL(file); // 파일 읽기
                reader.onload = function(){
                    FILE_ARRAY.push(file)
                };
                // 파일 목록을 화면에 추가
                const img_path =`<img src="/static/imgs/delete-doc.ico" width="20px" alt="문서삭제">`;
                let html_data = `
                <div class="filebox my-2 ml-2" id="file${FILE_NUM}">
                    <p class="name">
                        첨부${FILE_NUM + 1}: ${file.name}
                        <span>
                            <a class="delete" onclick="deleteFile(${FILE_NUM});">${img_path}</a>
                        </span>
                    </p>
                </div>`;
                $('.file-list').append(html_data)
                FILE_NUM++;
            } else{
                continue;
            }
        }
    }
    // 첨부 파일을 저장하였으므로 form input 내용 삭제
    $('input[type=file]').val('');

}

function saveFilesToForm(){
    let form = $('form');
    let form_data = new FormData(form[0]); //
    for (let i=0; i<FILE_ARRAY.length; i++){
        form_data.append('file', FILE_ARRAY[i]) // asr_file_views.py에서 'file'이라는 키값으로 접근하려고
    }
    return form_data;
}

// 첨부 파일 검증
function validation(obj){
    // 파일 타입 검사
    const fileTypes = [
        'audio/mpeg', // .mp3
        'video/x-msvideo', // .avi
        'audio/wav',
    ];
    // 지원하지 않는 파일 제외
    if(!fileTypes.includes(obj.type)){
        alert("지원하지 않는 파일 형식입니다. 첨부 불가 파일은 제외되었습니다.");
        return false;
    }    
    else if(obj.name.length > 200) { // 파일명 너무 길면 리젝
        alert("파일명 길이가 200자 이상인 파일은 제외되었습니다.")
        return false
    }   
    else if(obj.size > (500 * 1024 * 1024)) { // 파일 크기 제한
        alert("파일명 크기가 500MB 초과한 파일은 제외되었습니다.")
        return false
    }
    else if(obj.name.lastIndexOf('.')==-1) { // 확장가 없는 파일 제외
        alert("확장자가 없는 파일은 제외되었습니다.")
        return false
    }
    else{
        return true;
    }
}

function deleteFile(num){
    $("#file"+num).remove();
    FILE_ARRAY.splice(num, 1) // slice와 유사, num idx부터 1개 지움
    FILE_NUM--;
}

function get_user_id(){
    // 시간 정보 이용하여 uniqu한 id 생성
    const date = new Date();
    const user_id = 
        // ex. '2026-04-16_163559_1234
        date.getFullYear()
        + '-' + date.getMonth()
        + '-' +  date.getDate()
        + '_' + date.getHours()
        + date.getMinutes()
        + date.getSeconds()
        + '_' + date.getMilliseconds()
    return user_id
}

// 서버 전송 코드
$(function(){ // document(html)이 준비되었을 때 바로 실행됨 (사용자가 언제 서버 전송하기 버튼을 누를지 모르기 때문에 계속 대기)
    const result_text_area = $('#result_text_area');
    result_text_area.attr('hidden', true)
    // '서버 전송하기' 버튼 클릭되면
    // user_id = 생성 <- get_user_id()
    // upload
    // 만약 업로드 성공하면
        // ASR 수행 요청 -> process 함수
    let submit_btn = $('#submit_files');
    submit_btn.on('click', function(e){
        // 파일이 첨부되어 있는지 확인 
        //  서버에서 체크할 수도 있지만 서버는 바쁘니까 유저 컴(js)에서
        if (FILE_NUM===0){ // === 는 값('0') 뿐만 아니라 type도 일치하는지
            alert('첨부파일이 없습니다.\n분석할 파일을 추가해 주세요.')
            return;
        } 
        // 파일 첨부 영역 감추기, 업로드 스피터 시작
        $('#attach_area').attr('hidden', true);
        $('#p_par_area_process').attr('hidden', false);

        // 파이을 서버로 전송
        let form_data = saveFilesToForm();
        let user_id = get_user_id();
        $.ajax({ // 통신 지원
            method: 'POST',
            url: `/asr_file/upload/${user_id}`,
            data: form_data,
            dataType: 'json',// 서버(asr_file_views.py의 upload())로부터 받을 데이터 형식
            contentType: false, // asr_file_views.py의 upload()로 보내는 데이터 형식. 파일로 보내니까 false
            processData: false, // 보내기전에 클라이언트에서 파일을 전처리 못하게
            cache: false,
            success: function(result){ //asr_file_views.py의 upload()로부터 reponse가 잘 온 경우. asr_file_views.py의 upload() 반환값을 result가 받음
                console.log(result['status'])
                $('#p_par_area_upload').attr('hidden', true);
                $('#p_par_area_process').attr('hidden', false);
                $('#result_text_area').attr('hidden', false);
                process(user_id)
            },
            error: function(error){
                alert('에러가 발생했습니다. 관리자에게 문의해 주세요')
                console.log(error.status, error.statusText)
            }
        });  

    });

    $('#clear-content-btn').on('click', function(){
        location.reload();
    })

    $('#new-task-btn').on('click', function(){
        location.reload();
    })
});

function process(user_id){
    // 서버로 ASR 수행 요청 보냄
    // 텍스트 데이터가 도착 성공하면
    // -> html (브라우저)에 시현
    // 실패하면 -> 에러 발생... 관리자에게 문의해 주세요...
    $.ajax({
        method: 'POST',
        url: '/asr_file/process',
        data: JSON.stringify({'user_id': user_id}),
        dataType: 'json',
        contentType: 'application/json',
        success: function(result){
            console.log(result)
            $('#p_par_area_process').attr('hidden', true);
            $('#textarea_label').remove();
            $('#floatingTextarea2').val(result['0']);
            $('#new-task-btn').attr('hidden', false);
            
        },
        error: function(error){
            alert('에러가 발생했습니다. 관리자에게 문의해 주세요')
            console.log(error.status, error.statusText)
            location.href = '/asr_file';
        }
    });   
}