import string
import os
import sys

struct_list = [
    "timeval",
    "timezone",
    "timex",
    "tms",
    "timespec",
    "itimerval",
    "sigevent",
    "itimerspec",
    "sched_param",
    "kexec_segment",
    "rusage",
    "siginfo",
    "statfs",
    "statfs64",
    "stat",
    "ustat",
    "stat64",
    "io_event",
    "iocb",
    "utimbuf",
    "iovec",
    "linux_dirent",
    "linux_dirent64",
    "sockaddr",
    "msghdr",
    "mmsghdr",
    "pollfd",
    "sel_arg_struct",
    "epoll_event",
    "new_utsname",
    "rlimit",
    "rlimit64",
    "msgbuf",
    "msqid_ds",
    "sembuf",
    "shmid_ds",
    "mq_attr",
    "__sysctl_args",
    "robust_list_head",
    "getcpu_cache",
    "perf_event_attr",
    "mmap_arg_struct",
    "file_handle"
]

ioctl_struct_list = [
    "qseecom_register_listener_req",
    "qseecom_send_cmd_req",
    "qseecom_send_modfd_cmd_req",
    "qseecom_load_img_req",
    "qseecom_set_sb_mem_param_req",
    "qseecom_qseos_version_req",
    "qseecom_qseos_app_load_query",
    "venc_ioctl_msg"
]


head = "/***** Automatically generated by gen_recursive.c *********/\n\n#include <stdio.h>\n#include <time.h>\n#include <sys/types.h>\n#include <sys/stat.h>\n#include <fcntl.h>\n#include <sys/mman.h>\n#include <libxml/xmlwriter.h>\n#include <libxml/encoding.h>\n#include <sys/times.h>\n#include <sched.h>\n#include <linux/kexec.h>\n#include <sys/time.h>\n#include <sys/resource.h>\n#include <sys/vfs.h>\n#include <sys/syscall.h>\n#include <linux/aio_abi.h>\n#include <unistd.h>\n#include <utime.h>\n#include <dirent.h>\n#include <stdlib.h>\n#include <netinet/in.h>\n#include <poll.h>\n#include <sys/epoll.h>\n#include <sys/utsname.h>\n#ifdef LOLLIPOP\n#include <sys/msg.h>\n#include <sys/timex.h>\n#endif\n#include <sys/ipc.h>\n#include <linux/shm.h>\n#include <linux/futex.h>\n#include <linux/fs.h>\n#include <linux/sysctl.h>\n\n#include \"struct_analyze.h\"\n#include \"syscall.h\"\n#include \"ioctl_types.h\"\n\nint nullfd = 0;\n\nvoid struct_recursive_analyze(void *arg_ptr, bool is_ioctl_call, enum ioctl_struct_type ioctl_struct_type, enum struct_argtype struct_argtype, xmlTextWriterPtr writer) {\n\nif(arg_ptr == NULL)\nreturn;\nif(nullfd == 0)\nnullfd = open(\"/dev/random\", O_WRONLY);\n\nif(is_ioctl_call == TRUE) {\nswitch(ioctl_struct_type) {\n"


f = open("test.c", "w")
f.write(head)

k = 0
for i in ioctl_struct_list:
    f.write("struct " + i + " *p" + str(k) + ";\n")
    k = k + 1


f.write("case STRUCT_undefined:\n\nreturn;\n\n")

k = 0
for i in ioctl_struct_list:
    f.write("case STRUCT_" + i + ":\n")
    f.write("if(write(nullfd, (void *) arg_ptr, sizeof(struct " + i + ")) < 0) {\n")
    f.write("xmlTextWriterWriteElement(writer, \"STRUCT_" + i + "\", \"unmapped\");\n")
    f.write("return;\n }\n\n")

    f.write("p" + str(k) + " = (struct " + i + " *) arg_ptr;\n")
    f.write("xmlTextWriterStartElement(writer, \"STRUCT_" + i + "\");\n")
    f.write("xmlTextWriterWriteBase64(writer, (char *) " + "p" + str(k) + " , 0, sizeof(struct " + i + "));\n")
    f.write("xmlTextWriterEndElement(writer);\n\n")
    f.write("return;\n\n")

    k = k + 1

f.write("default:\nreturn;\n}\n}\n\n#ifdef LOLLIPOP\n\nswitch(struct_argtype) {\n")


for i in struct_list:
    f.write("struct " + i + " " + i + "_s;\n")
    f.write("struct " + i + " *" + i + "_p;\n\n")


for i in struct_list:
    f.write("case STRUCT_ARG_" + i + ":\n")
    f.write("if(write(nullfd, (void *) arg_ptr, sizeof(" + i + "_s"  +")) < 0) {\n")
    f.write("xmlTextWriterWriteElement(writer, \"STRUCT_" + i + "\", \"unmapped\");\n")
    f.write("return;\n }\n\n")

    f.write(i + "_p = (struct " + i + " *) arg_ptr;\n")
    f.write("xmlTextWriterStartElement(writer, \"STRUCT_" + i + "\");\n")
    f.write("xmlTextWriterWriteBase64(writer, (char *) " + i + "_p, 0, sizeof(" + i + "_s));\n")
    f.write("xmlTextWriterEndElement(writer);\n\n")
    f.write("break;\n\n")
        

f.write("default:\nbreak;\n}\n#endif\n}")
f.close()
