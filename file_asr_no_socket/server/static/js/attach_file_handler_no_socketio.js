/* 참고문서
    1. https://purecho.tistory.com/68
    2. https://codepen.io/green526/embed/qBjZLex?height=537&default-tab=html%2Cresult&slug-hash=qBjZLex&editable=true&user=green526&ke-size=size16&name=cp_embed_1
*/

var FILE_NUM = 0; // 첨부된 파일 개수
var FILE_ARRAY = new Array(); // 첨부 파일 저장용 배열

function addFile(obj){
    let max_file_count = 10; // 첨부팡리 최대 개수
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

// 서버 전송 코드