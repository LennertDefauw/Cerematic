from subprocess import check_output


class IPaddress():
    def get_IP(self):
        ips = check_output(['hostname', '--all-ip-addresses'])
        return str(ips)
        # ips = str(ips).split(" ")[0:2]

        # for item in ips:
        #     array.append(item)
        #
        # specialip = array[0]
        # withoutb = specialip[2:]
        #
        # ipadresses = withoutb + "    " + str(array[1])
        # return ipadresses


