import math

# conv_idx, nif, pof, k, s, nox, noy
conv_precision_arg_idx = 1
conv_nif_arg_idx = 2
conv_nof_arg_idx = 3
conv_k_arg_idx = 4
conv_s_arg_idx = 5
conv_nox_arg_idx = 6
conv_noy_arg_idx = 7

conv_layers_args = [
    [1, 0, 3, 32, 3, 2, 512, 512],
    [2, 0, 32, 64, 3, 2, 256, 256],
    [3, 0, 64, 32, 1, 1, 256, 256],
    [4, 0, 32, 32, 1, 1, 256, 256],
    [5, 0, 32, 32, 3, 1, 256, 256],
    [6, 0, 64, 32, 1, 1, 256, 256],
    [7, 0, 64, 64, 1, 1, 256, 256],
    [8, 0, 64, 128, 3, 2, 128, 128],
    [9, 0, 128, 64, 1, 1, 128, 128],
    [10, 0, 64, 64, 1, 1, 128, 128],
    [11, 0, 64, 64, 3, 1, 128, 128],
    [12, 0, 64, 64, 1, 1, 128, 128],
    [13, 0, 64, 64, 3, 1, 128, 128],
    [14, 0, 128, 64, 1, 1, 128, 128],
    [15, 0, 128, 128, 1, 1, 128, 128],
    [16, 0, 128, 256, 3, 2, 64, 64],
    [17, 0, 256, 128, 1, 1, 64, 64],
    [18, 0, 128, 128, 1, 1, 64, 64],
    [19, 0, 128, 128, 3, 1, 64, 64],
    [20, 0, 128, 128, 1, 1, 64, 64],
    [21, 0, 128, 128, 3, 1, 64, 64],
    [22, 0, 128, 128, 1, 1, 64, 64],
    [23, 0, 128, 128, 3, 1, 64, 64],
    [24, 0, 256, 128, 1, 1, 64, 64],
    [25, 0, 256, 256, 1, 1, 64, 64],
    [26, 0, 256, 512, 3, 2, 32, 32],
    [27, 0, 512, 256, 1, 1, 32, 32],
    [28, 0, 256, 256, 1, 1, 32, 32],
    [29, 0, 256, 256, 3, 1, 32, 32],
    [30, 0, 512, 256, 1, 1, 32, 32],
    [31, 0, 512, 512, 1, 1, 32, 32],
    [32, 0, 512, 256, 1, 1, 32, 32],
    [33, 0, 1024, 512, 1, 1, 32, 32],
    [34, 0, 512, 256, 1, 1, 32, 32],
    [35, 0, 512, 128, 1, 1, 64, 64],
    [36, 0, 128, 128, 1, 1, 64, 64],
    [37, 0, 128, 128, 3, 1, 64, 64],
    [38, 0, 512, 128, 1, 1, 64, 64],
    [39, 0, 256, 256, 1, 1, 64, 64],
    [40, 0, 256, 128, 1, 1, 64, 64],
    [41, 0, 256, 64, 1, 1, 128, 128],
    [42, 0, 64, 64, 1, 1, 128, 128],
    [43, 0, 64, 64, 3, 1, 128, 128],
    [44, 0, 256, 64, 1, 1, 128, 128],
    [45, 0, 128, 128, 1, 1, 128, 128],
    [46, 0, 128, 128, 3, 2, 64, 64],
    [47, 0, 256, 128, 1, 1, 64, 64],
    [48, 0, 128, 128, 1, 1, 64, 64],
    [49, 0, 128, 128, 3, 1, 64, 64],
    [50, 0, 256, 128, 1, 1, 64, 64],
    [51, 0, 256, 256, 1, 1, 64, 64],
    [52, 0, 256, 256, 3, 2, 32, 32],
    [53, 0, 512, 256, 1, 1, 32, 32],
    [54, 0, 256, 256, 1, 1, 32, 32],
    [55, 0, 256, 256, 3, 1, 32, 32],
    [56, 0, 512, 256, 1, 1, 32, 32],
    [57, 0, 512, 512, 1, 1, 32, 32],
    [58, 0, 128, 255, 1, 1, 128, 128],
    [59, 0, 256, 255, 1, 1, 64, 64],
    [60, 0, 512, 255, 1, 1, 32, 32]
    ]

#w8a8
pox=32
pixel_bits = 8
ddr_bits_per_cycle = 512

pof_min = 16
pof_max = 64

pof_set = []
poy_set = []
tile_latency_set = []
tile_num_set = []
layer_latency_set = []
pe_util_set = []

total_latency = 0
theoritical_latency=0
dsp_num = 96


for i in range (1, 61):
    precision_mode = conv_layers_args[i-1][conv_precision_arg_idx]
    nif = conv_layers_args[i-1][conv_nif_arg_idx]
    nof = conv_layers_args[i-1][conv_nof_arg_idx]
    k = conv_layers_args[i-1][conv_k_arg_idx]
    s = conv_layers_args[i-1][conv_s_arg_idx]
    nox = conv_layers_args[i-1][conv_nox_arg_idx]
    noy = conv_layers_args[i-1][conv_noy_arg_idx]

    tof = nof

    layer_latency_w1a8_accumulate = 0
    dsp_util_w1a8_accumulate = 0

    layer_latency_w8a8_accumulate = 0
    dsp_util_w8a8_accumulate = 0

    while tof > 0: #对nof分块,这样可以减少块的数量
        #每个计算任务的最短延迟的要求,计算覆盖传输的要求

        SP_min = 1
        SP_max = min(nox * noy, dsp_num) if precision_mode == 0 else min(nox * noy, dsp_num * 2)

        FP_min = 1
        # FP_max = min(nof, dsp_num * 2)
        FP_max = min(tof, dsp_num * 2)

        mac_throughput_w8 = dsp_num * 2
        mac_throughput_w1 = dsp_num * 4

        #figure out the optimal key

        SP_mult_FP_DDR_limit_SP_min = nif * ddr_bits_per_cycle * k * k / pixel_bits - nif * SP_min * s * s 

        SP_mult_FP_arg_limit_SP_min = SP_min * FP_max

        if SP_mult_FP_DDR_limit_SP_min >= SP_mult_FP_arg_limit_SP_min:
            #SP_min * FP_max can satisfy the com-ld_str overlap, we need to up the SP, to make SP*FP bigger possible
            FP_overlap = FP_max
            SP_overlap = math.floor((nif * ddr_bits_per_cycle * k * k) / pixel_bits / (FP_overlap + (nif * s * s)))

        else:
            #parrallel in SP_min * FP_max can never satisfy the com-ld_str overlap, need to reduce the FP_max
            SP_overlap = SP_min
            FP_overlap = SP_mult_FP_DDR_limit_SP_min / 1

        SP_mult_FP = FP_overlap * SP_overlap #maximum overlap parrallel
        print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
        print("transimition bits needed in a overlap time: %d"
            %((SP_overlap * nif * s * s + FP_overlap * SP_overlap) * pixel_bits))
        print("/////////////")

        computation_latency = nif * k * k

        layer_latency_w1a8 = 0
        layer_tile_num_w1a8 = 0
        tile_latency_w1a8 = 0
        tile_latency_type_w1a8 = ""
        dsp_util_w1a8 = 0

        layer_latency_w8a8 = 0
        layer_tile_num_w8a8 = 0
        tile_latency_w8a8 = 0
        tile_latency_type_w8a8 = ""
        dsp_util_w8a8 = 0

        if precision_mode == 1:
            #w1a8
            #model the latency
            if SP_mult_FP >= mac_throughput_w1:
                # flag = "optimize usage"
                #xxxxxx the resource is less than the posssible SP*FP

                FP = FP_overlap
                SP = mac_throughput_w1 / FP
                # layer_tile_num_overlap = math.ceil(nox * noy / SP) * math.ceil(nof / FP)
                layer_tile_num_overlap = math.ceil(nox * noy / SP)
                layer_latency_overlap = layer_tile_num_overlap * computation_latency / 150 / 1000

                layer_latency_w1a8 = layer_latency_overlap
                layer_tile_num_w1a8 = layer_tile_num_overlap
                tile_latency_w1a8 = computation_latency / 150 / 1000
                tile_latency_type_w1a8 = "computation delay"
                dsp_util_w1a8 = FP * SP / mac_throughput_w1

                print("layer_tile_num_overlap=%4d, tile_delay=%8d, layer_latency_overlap=%f"
                    %(layer_tile_num_overlap, computation_latency, layer_latency_overlap))
                print("optimize usage: computation_delay=%f"
                    %(layer_latency_overlap))
                
                print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                print("transimition bits needed in a overlap time: %d"
                    %((SP * nif * s * s + FP * SP) * pixel_bits))
                print("§§§§§§§§§§§")

                print("cv_idx=%3d, w1a8, nif=%4d, nof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w1=%d"
                        %(i, nif, nof, k, s, nox, noy, SP_mult_FP, mac_throughput_w1))
                print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                    %(SP, FP, layer_latency_w1a8, layer_tile_num_w1a8, tile_latency_w1a8, tile_latency_type_w1a8, dsp_util_w1a8))
                print("a FP tile--------------------------")

                tof = tof - FP
                layer_latency_w1a8_accumulate = layer_latency_w1a8_accumulate + layer_latency_w1a8
                dsp_util_w1a8_accumulate = dsp_util_w1a8_accumulate + dsp_util_w1a8 * layer_latency_w1a8

            #for the below conditions
            #eval the total latency to decide the final SP * FP
            #SP_mult_FP is the maximum val that trans can be fully overlaped, so the tile latency is com_latency
            #if make SP_mult_FP bigger, the tile latency grows but the num of tiles drops, so eval the total latency 
            else:
                #flag = "w1 less than 100%% opt usage"
                # layer_tile_num_overlap = math.ceil(nox * noy / SP_overlap) * math.ceil(nof / FP_overlap)
                layer_tile_num_overlap = math.ceil(nox * noy / SP_overlap)
                layer_latency_overlap = layer_tile_num_overlap * computation_latency / 150 / 1000

                #if FP * SP > SP_mult_FP, then make FP as great as possible
                FP_dsp_util = FP_max
                # SP_dsp_util = math.floor(mac_throughput_w1 / FP_dsp_util) #might be small?
                SP_dsp_util = SP_overlap ## reduce power but keep the latency
                # layer_tile_num_dsp_util = math.ceil(nox * noy/ SP_dsp_util) * math.ceil(nof / FP_dsp_util)
                layer_tile_num_dsp_util = math.ceil(nox * noy/ SP_dsp_util)
                transmition_latency = (SP_dsp_util * s * s * nif + FP_dsp_util * SP_dsp_util) * pixel_bits / ddr_bits_per_cycle
                layer_latency_dsp_util = layer_tile_num_dsp_util * transmition_latency / 150 / 1000

                print("layer_tile_num_overlap=%4d, tile_delay=%8d, layer_latency_overlap=%f"
                    %(layer_tile_num_overlap, computation_latency, layer_latency_overlap))
                print("layer_tile_num_dsp_util=%4d, tile_delay=%8d, layer_latency_dsp_util=%f"
                    %(layer_tile_num_dsp_util, transmition_latency, layer_latency_dsp_util))
                print("evaluate 2 delay: computation_delay=%f, transmition_delay=%f"
                    %(layer_latency_overlap, layer_latency_dsp_util))

                if layer_latency_overlap <= layer_latency_dsp_util:
                    layer_latency_w1a8 = layer_latency_overlap
                    layer_tile_num_w1a8 = layer_tile_num_overlap
                    tile_latency_w1a8 = computation_latency / 150 / 1000
                    tile_latency_type_w1a8 = "computation delay"
                    dsp_util_w1a8 = SP_mult_FP / mac_throughput_w1
                    FP = FP_overlap
                    SP = SP_overlap
                    print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                    print("transimition bits needed in a overlap time: %d"
                        %((SP * nif * s * s + FP * SP) * pixel_bits))
                    print("§§§§§§§§§§§")
                    print("cv_idx=%3d, w1a8, nif=%4d, nof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w1=%d"
                        %(i, nif, nof, k, s, nox, noy, SP_mult_FP, mac_throughput_w1))
                    print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                        %(SP, FP, layer_latency_w1a8, layer_tile_num_w1a8, tile_latency_w1a8, tile_latency_type_w1a8, dsp_util_w1a8))
                    print("a FP tile--------------------------")

                    tof = tof - FP
                    layer_latency_w1a8_accumulate = layer_latency_w1a8_accumulate + layer_latency_w1a8
                    dsp_util_w1a8_accumulate = dsp_util_w1a8_accumulate + dsp_util_w1a8 * layer_latency_w1a8

                else:
                    layer_latency_w1a8 = layer_latency_dsp_util
                    layer_tile_num_w1a8 = layer_tile_num_dsp_util
                    tile_latency_w1a8 = transmition_latency / 150 / 1000
                    tile_latency_type_w1a8 = "transmition delay"
                    dsp_util_w1a8 = FP_dsp_util * SP_dsp_util / mac_throughput_w1
                    FP = FP_dsp_util
                    SP = SP_dsp_util
                    print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                    print("transimition bits needed in a overlap time: %d"
                        %((SP * nif * s * s + FP * SP) * pixel_bits))
                    print("§§§§§§§§§§§")
                    print("cv_idx=%3d, w1a8, nif=%4d, nof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w1=%d"
                        %(i, nif, nof, k, s, nox, noy, SP_mult_FP, mac_throughput_w1))
                    print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                        %(SP, FP, layer_latency_w1a8, layer_tile_num_w1a8, tile_latency_w1a8, tile_latency_type_w1a8, dsp_util_w1a8))
                    print("a FP tile--------------------------")
                    
                    tof = tof - FP
                    layer_latency_w1a8_accumulate = layer_latency_w1a8_accumulate + layer_latency_w1a8
                    dsp_util_w1a8_accumulate = dsp_util_w1a8_accumulate + dsp_util_w1a8 * layer_latency_w1a8

        else:
            #w8a8
            #model the latency
            if SP_mult_FP >= mac_throughput_w8:
                # flag = "optimize usage"
                #xxxxxx the resource is less than the posssible SP*FP
                FP = FP_overlap
                SP = mac_throughput_w8 / FP

                # layer_tile_num_overlap = math.ceil(nox * noy / SP) * math.ceil(nof / FP)
                layer_tile_num_overlap = math.ceil(nox * noy / SP)
                layer_latency_overlap = layer_tile_num_overlap * computation_latency / 150 / 1000

                layer_latency_w8a8 = layer_latency_overlap
                layer_tile_num_w8a8 = layer_tile_num_overlap
                tile_latency_w8a8 = computation_latency / 150 / 1000
                tile_latency_type_w8a8 = "computation delay"
                dsp_util_w8a8 = FP * SP / mac_throughput_w8

                print("layer_tile_num_overlap=%4d, tile_delay=%8d, layer_latency_overlap=%f"
                    %(layer_tile_num_overlap, computation_latency, layer_latency_overlap))
                print("optimize usage: computation_delay=%f"
                    %(layer_latency_overlap))
                
                print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                print("transimition bits needed in a overlap time: %d"
                    %((SP * nif * s * s + FP * SP) * pixel_bits))
                print("§§§§§§§§§§§")
            
                print("cv_idx=%3d, w8a8, nif=%4d, tof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w8=%d"
                        %(i, nif, tof, k, s, nox, noy, SP_mult_FP, mac_throughput_w8))
                print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                    %(SP, FP, layer_latency_w8a8, layer_tile_num_w8a8, tile_latency_w8a8, tile_latency_type_w8a8, dsp_util_w8a8))
                print("a FP tile--------------------------")

                tof = tof - FP
                layer_latency_w8a8_accumulate = layer_latency_w8a8_accumulate + layer_latency_w8a8
                dsp_util_w8a8_accumulate = dsp_util_w8a8_accumulate + dsp_util_w8a8 * layer_latency_w8a8


            #for the below conditions
            #eval the total latency to decide the final SP * FP
            #SP_mult_FP is the maximum val that trans can be fully overlaped, so the tile latency is com_latency
            #if make SP_mult_FP bigger, the tile latency grows but the num of tiles drops, so eval the total latency 
            else:
                #flag = "w8 less than 100%% opt usage"
                # layer_tile_num_overlap = math.ceil(nox * noy / SP_overlap) * math.ceil(nof / FP_overlap)
                layer_tile_num_overlap = math.ceil(nox * noy / SP_overlap)
                layer_latency_overlap = layer_tile_num_overlap * computation_latency / 150 / 1000

                #if FP * SP > SP_mult_FP, then make FP as great as possible
                FP_dsp_util = FP_max
                # SP_dsp_util = math.floor(mac_throughput_w8 / FP_dsp_util)  #might be small?
                SP_dsp_util = SP_overlap ## reduce power but keep the latency
                # layer_tile_num_dsp_util = math.ceil(nox * noy / SP_dsp_util) * math.ceil(nof / FP_dsp_util)
                layer_tile_num_dsp_util = math.ceil(nox * noy / SP_dsp_util)
                transmition_latency = (SP_dsp_util * s * s * nif + FP_dsp_util * SP_dsp_util) * pixel_bits / ddr_bits_per_cycle
                layer_latency_dsp_util = layer_tile_num_dsp_util * transmition_latency / 150 / 1000
                
                print("layer_tile_num_overlap=%4d, tile_delay=%8d, layer_latency_overlap=%f"
                    %(layer_tile_num_overlap, computation_latency, layer_latency_overlap))
                print("layer_tile_num_dsp_util=%4d, tile_delay=%8d, layer_latency_dsp_util=%f"
                    %(layer_tile_num_dsp_util, transmition_latency, layer_latency_dsp_util))
                print("evaluate 2 delay: computation_delay=%f, transmition_delay=%f"
                    %(layer_latency_overlap, layer_latency_dsp_util))

                if layer_latency_overlap <= layer_latency_dsp_util:
                    layer_latency_w8a8 = layer_latency_overlap
                    layer_tile_num_w8a8 = layer_tile_num_overlap
                    tile_latency_w8a8 = computation_latency / 150 / 1000
                    tile_latency_type_w8a8 = "computation delay"
                    dsp_util_w8a8 = SP_mult_FP / mac_throughput_w8
                    FP = FP_overlap
                    SP = SP_overlap
                    print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                    print("transimition bits needed in a overlap time: %d"
                        %((SP * nif * s * s + FP * SP) * pixel_bits))
                    print("§§§§§§§§§§§")
                    print("cv_idx=%3d, w8a8, nif=%4d, tof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w8=%d"
                        %(i, nif, tof, k, s, nox, noy, SP_mult_FP, mac_throughput_w8))
                    print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                        %(SP, FP, layer_latency_w8a8, layer_tile_num_w8a8, tile_latency_w8a8, tile_latency_type_w8a8, dsp_util_w8a8))
                    print("a FP tile--------------------------")

                    tof = tof - FP
                    layer_latency_w8a8_accumulate = layer_latency_w8a8_accumulate + layer_latency_w8a8
                    dsp_util_w8a8_accumulate = dsp_util_w8a8_accumulate + dsp_util_w8a8 * layer_latency_w8a8

                else:
                    layer_latency_w8a8 = layer_latency_dsp_util
                    layer_tile_num_w8a8 = layer_tile_num_dsp_util
                    tile_latency_w8a8 = transmition_latency / 150 / 1000
                    tile_latency_type_w8a8 = "transmition delay"
                    dsp_util_w8a8 = FP_dsp_util * SP_dsp_util / mac_throughput_w8
                    FP = FP_dsp_util
                    SP = SP_dsp_util
                    print("transimition throughput in a overlap time: %d"
                    %(nif * k * k * ddr_bits_per_cycle))
                    print("transimition bits needed in a overlap time: %d"
                        %((SP * nif * s * s + FP * SP) * pixel_bits))
                    print("§§§§§§§§§§§")
                    print("cv_idx=%3d, w8a8, nif=%4d, tof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d, SP_mult_FP<=%f, mac_throughput_w8=%d"
                        %(i, nif, tof, k, s, nox, noy, SP_mult_FP, mac_throughput_w8))
                    print("SP=%4d, FP=%4d, layer_latency=%f, layer_tile_num=%4d, tile_latency=%f, %s, dsp_util=%f"
                        %(SP, FP, layer_latency_w8a8, layer_tile_num_w8a8, tile_latency_w8a8, tile_latency_type_w8a8, dsp_util_w8a8))
                    print("a FP tile--------------------------")

                    tof = tof - FP
                    layer_latency_w8a8_accumulate = layer_latency_w8a8_accumulate + layer_latency_w8a8
                    dsp_util_w8a8_accumulate = dsp_util_w8a8_accumulate + dsp_util_w8a8 * layer_latency_w8a8

    if precision_mode == 1:
        dsp_util_w1a8_accumulate = dsp_util_w1a8_accumulate / layer_latency_w1a8_accumulate
        print("cv_idx=%3d, w1a8, nif=%4d, nof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d"
                %(i, nif, nof, k, s, nox, noy))
        print("layer_latency_w1a8_accumulate=%f, dsp_util_w1a8_accumulate=%f"
            %(layer_latency_w1a8_accumulate, dsp_util_w1a8_accumulate))
        print("a layer---------------------------------------------------")
    
    else:
        dsp_util_w8a8_accumulate = dsp_util_w8a8_accumulate / layer_latency_w8a8_accumulate
        print("cv_idx=%3d, w8a8, nif=%4d, nof=%4d, k=%2d, s=%2d, nox=%4d, noy=%4d"
                %(i, nif, nof, k, s, nox, noy))
        print("layer_latency_w8a8_accumulate=%f, dsp_util_w8a8_accumulate=%f"
            %(layer_latency_w8a8_accumulate, dsp_util_w8a8_accumulate))
        print("a layer---------------------------------------------------")

    #figure out by search

    FP_key = 0
    SP_key = 0
    layer_latency_key = 1000 #1000ms
    for FP_iter in range(FP_max, FP_min - 1, -1):
        SP_limit = min(nox * noy, dsp_num, mac_throughput_w8//FP_iter) if precision_mode == 0 else min(nox * noy, dsp_num*2, mac_throughput_w1//FP_iter)

        for SP_iter in range(SP_limit, SP_min-1, -1):
            transimition_throughput = nif * k * k * ddr_bits_per_cycle
            transimition_bits = (SP_iter * nif * s * s + FP_iter * SP_iter) * pixel_bits
    
            if transimition_throughput >= transimition_bits:
                #transmition can be overlap by computation
                tile_latency = nif * k * k
            else:
                tile_latency = math.ceil(transimition_bits / ddr_bits_per_cycle)

            layer_latency = math.ceil(nox * noy / SP_iter) * math.ceil(nof / FP_iter) * tile_latency / 150 / 1000

            if layer_latency < layer_latency_key:
                layer_latency_key = layer_latency
                FP_key = FP_iter
                SP_key = SP_iter
    
    print("SP=%4d, FP=%4d, layer_latency=%f"
                    %(SP_key, FP_key, layer_latency_key))
    print("***********************************************************")


