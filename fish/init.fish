source (dirname (status -f))/git-aliases.fish

set TERM xterm-256color
set -g theme_title_display_process yes
set -g theme_show_exit_status yes
set fish_color_command '2585ff'  '--bold'
set fish_color_match cyan  '--bold'
set fish_color_operator cyan  '--bold'
set fish_color_escape cyan  '--bold'

function ak_echo_header
    set echo_color $argv[1]
    set_color $echo_color --bold
    echo "--------------------------------------------------------------------------------"
    set_color $echo_color
    echo "$argv[2]" | sed "s/$argv[3]/$argv[4]/g"
    set_color $echo_color --bold
    echo "--------------------------------------------------------------------------------"
    set_color normal
end

alias ak_colorbuild='colout -T ~/env/colout -t buildcolors'

function ak_build
    set var_ccache_prefix $argv[1]
    set var_jobs $argv[2]
    set var_target $argv[3]
    set var_contractor_args $argv[4..-1]
    set build_cmd "env CCACHE_PREFIX=\"$var_ccache_prefix\" NINJA_STATUS=\"[%p]{%t} \" ICECC_CARET_WORKAROUND=\"0\" \
ninja $var_target -j$var_jobs -k1 ^&1 | \
colout -T ~/env/colout/ -t buildcolors | \
~/projects/sandbox/env/contractor.py $var_contractor_args"
    ak_echo_header cyan $build_cmd "|" "|\n"
    ak_buildinfo
    set number_edges (ninja $var_target -n | sed "s/^.*\/\([0-9]\+\)\].*\$/\1/g" | head -n1)
    if [ $number_edges -eq 1 ]
        set_color yellow --bold
        echo "-------------------------------------------"
        echo "Something got updated, configuring first..."
        echo "-------------------------------------------"
        set_color normal
        ninja rebuild_cache | ak_colorbuild
        set number_edges (ninja $var_target -n | sed "s/^.*\/\([0-9]\+\)\].*\$/\1/g" | head -n1)
        ak_buildinfo
    end
    set_color yellow --bold
    echo "Executing $number_edges edges"
    set_color normal
    echo
    sleep 1
    eval $build_cmd; or true
    notify-send -u normal -i geany-build -t 15000 "Build Finished"
end

alias ak_formatdiff='git diff -U0 HEAD^ | clang-format-diff-3.7 -i -p1; gg'
alias ak_rebuildcache='ninja rebuild_cache ^&1 | ak_colorbuild'
alias ak_repo_checkout_current="git co (repo info . | grep \"Current revision: \" | sed \"s/Current revision: \(.*\)/\1/g\")"
alias ak_grep_cmake="ag $argv[1] -i -G \"(CMakeLists.txt|.*\.cmake)\""
alias jekyll='docker run --rm -p 127.0.0.1:4000:4000 --volume=$PWD:/srv/jekyll -it jekyll/jekyll jekyll'

alias teto=ak_build
alias fgg=ak_formatdiff
alias clipboard='xsel -ib'
