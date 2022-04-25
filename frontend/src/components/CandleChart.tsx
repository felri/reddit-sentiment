import React, { FC, useEffect, useState, useRef } from "react";
import styles from "./styles/Button.module.css";
import classNames from "classnames";
import ReactApexChart from "react-apexcharts";
import ApexCharts from "apexcharts";
import { DataChart } from "../utils/types";

type Props = {
  dataChart?: DataChart | null;
  loading: boolean;
  commentDate: string | number | null;
};

export const CandleChart: FC<Props> = ({
  dataChart,
  loading,
  commentDate,
}: Props) => {
  const [series, setSeries] = useState<any>([
    {
      data: [],
    },
  ]);
  const [options, setOptions] = useState<any>({
    chart: {
      type: "candlestick",
      height: 290,
      id: "candles",
      toolbar: {
        autoSelected: "pan",
        show: false,
      },
      zoom: {
        enabled: true,
      },
      labels: {
        color: "white",
      },
    },
    annotations: {
      xaxis: [
        {
          x: commentDate,
          borderColor: "#00E396",
          label: {
            color: "white",
            borderColor: "#00E396",
            style: {
              fontSize: "12px",
              color: "white",
              background: "#00E396",
            },
            orientation: "horizontal",
            offsetY: 7,
          },
        },
      ],
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: "#3C90EB",
          downward: "#DF7D46",
        },
      },
    },
    xaxis: {
      type: "datetime",
    },
  });
  const [seriesBar, setSeriesBar] = useState<any>([
    {
      name: "volume",
      data: [],
    },
  ]);
  const [optionsBar, setOptionsBar] = useState<any>({
    optionsBar: {
      chart: {
        height: 160,
        type: "bar",
        brush: {
          enabled: true,
          target: "candles",
        },
        selection: {
          enabled: true,
          xaxis: {
            min: new Date("20 Jan 2017").getTime(),
            max: new Date("10 Dec 2017").getTime(),
          },
          fill: {
            color: "#ccc",
            opacity: 0.4,
          },
          stroke: {
            color: "#0D47A1",
          },
        },
      },
      dataLabels: {
        enabled: false,
      },
      plotOptions: {
        bar: {
          columnWidth: "80%",
          colors: {
            ranges: [
              {
                from: -1000,
                to: 0,
                color: "#F15B46",
              },
              {
                from: 1,
                to: 10000,
                color: "#FEB019",
              },
            ],
          },
        },
      },
      stroke: {
        width: 0,
      },
      xaxis: {
        type: "datetime",
        axisBorder: {
          offsetX: 13,
        },
      },
      yaxis: {
        labels: {
          show: false,
        },
      },
    },
  });

  useEffect(() => {
    if (dataChart) {
      const { series, linear } = dataChart;
      setSeries([{ data: series.slice(-250) }]);
      setSeriesBar([{ name: "volume", data: linear.slice(-250) }]);
    } else {
      setSeries(null);
      setOptions(null);
    }
    if (commentDate && series[0].data.length > 0) {
      const aux = { ...options };
      aux.annotations.xaxis[0].x = new Date(commentDate).getTime();
      ApexCharts.exec("candles", "updateOptions", aux);
      setOptions(aux);
    }
  }, [dataChart?.series, dataChart?.linear, commentDate]);

  return (
    <div className={styles.container}>
      <div className="container" style={{ height: "calc(100% - 25px)" }}>
        <div id="chart-candlestick">
          {series[0].data.length > 0 && (
            <ReactApexChart
              options={options}
              series={series}
              type="candlestick"
              height={800}
            />
          )}
        </div>
      </div>
    </div>
  );
};
