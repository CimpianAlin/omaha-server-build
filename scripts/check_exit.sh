
function check_exit() {
    return=$?;
    if [[ $return -eq 0 ]]; then
	echo "[INFO] $0 succeded"
    else
	echo "[ERROR] $0 failed"
    fi

    exit $return
}

trap check_exit EXIT
