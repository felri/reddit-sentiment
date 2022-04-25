import React, { FC, useMemo } from "react";
import { Comment, DataChart } from "../utils/types";
import styles from "./styles/Comments.module.css";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from "react-responsive-carousel";
import { useEventListener } from "../utils/hooks";
import { Button } from "../components/Button";
import { CandleChart } from "../components/CandleChart";

type Props = {
  pressedButton: string;
};

const Buttons: FC<any> = ({ pressedButton }: Props) => {
  return (
    <div className={styles.buttons}>
      <Button
        pressedButton={pressedButton}
        predictionNumber={1}
        button={"bearish"}
      />
      <Button
        pressedButton={pressedButton}
        predictionNumber={2}
        button={"neutral"}
      />
      <Button
        pressedButton={pressedButton}
        predictionNumber={3}
        button={"bullish"}
      />
      <Button
        pressedButton={pressedButton}
        predictionNumber={4}
        button={"delete"}
      />
    </div>
  );
};

export const Protected: FC = () => {
  const [comments, setComments] = React.useState<Array<Comment>>([]);
  const [dataChart, setDataChart] = React.useState<DataChart | null>();
  const [currentSlide, setCurrentSlide] = React.useState<number>(0);
  const [keyboardBeingPressed, setKeyboardBeingPressed] =
    React.useState<string>("");
  const [loading, setLoading] = React.useState<boolean>(true);
  const [loadingChart, setLoadingChart] = React.useState<boolean>(true);

  const fetchChartByTicket = async (ticketId: number) => {
    try {
      const response = await fetch("/api/v1/charts/" + ticketId, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });
      let data = await response.json();
      data = modifyChartData(data);
      setDataChart(data);
      setLoadingChart(false);
    } catch (error) {
      console.log(error);
    }
  };

  const noDecimals = (number: number) => {
    return Math.round(number * 100) / 100;
  };

  const modifyChartData = (data: Array<any>) => {
    const series = data.map((item: any) => {
      return {
        x: item.date.substring(0, item.date.length - 9),
        y: [
          noDecimals(item.open),
          noDecimals(item.high),
          noDecimals(item.low),
          noDecimals(item.close),
        ],
      };
    });

    const linear = data.map((item: any) => {
      return {
        x: item.date.substring(0, item.date.length - 9),
        y: noDecimals(item.volume),
      };
    });

    return { series, linear };
  };

  const fetchComments = async () => {
    try {
      const offset = comments.length;
      const limit = 100;
      const response = await fetch("/api/v1/comments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          offset,
          limit,
        }),
      });
      const data = await response.json();
      setComments(comments.concat(data));
      setLoading(false);
    } catch (error) {
      console.log(error);
    }
  };

  const unixToDate = (unix: string | undefined) => {
    if (!unix) return new Date().toString();
    const date = new Date(Number(unix) * 1000);
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
  };

  const updatePredictionComment = async (
    prediction: number,
    comment: Comment | null
  ) => {
    try {
      const body = { ...comment, prediction };
      const response = await fetch("/api/v1/comments/" + comment?.id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(body),
      });
      const data = await response.json();

      const updatedComments = comments.map((c) => {
        if (c?.id === data.id) {
          return data;
        }
        return c;
      });
      setComments(updatedComments);
      setCurrentSlide((f) => f + 1);
    } catch (error) {
      console.log(error);
    }
  };

  const deleteComment = async (id: number | undefined) => {
    if (!id) return;
    try {
      await fetch(`/api/v1/comments/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });
      setComments(comments.filter((comment) => comment?.id !== id));
    } catch (error) {
      console.log(error);
    }
  };

  const listenKeyboardDown = (e: KeyboardEvent) => {
    setKeyboardBeingPressed(e.key);
    setTimeout(() => {
      setKeyboardBeingPressed("");
    }, 200);

    if (e.key === "ArrowLeft") setCurrentSlide((f) => f - 1);
    if (e.key === "ArrowRight") setCurrentSlide((f) => f + 1);

    if (e.key === "d") deleteComment(comments[currentSlide]?.id);
    if (
      e.key === "1" ||
      e.key === "2" ||
      e.key === "3" ||
      e.key === "4" ||
      e.key === "5"
    ) {
      updatePredictionComment(Number(e.key), comments[currentSlide]);
    }
  };

  const handleSwipe = (i: number) => {
    setCurrentSlide(i);
  };

  const selectedCommentDate = useMemo(() => {
    if (comments[currentSlide]) {
      return unixToDate(comments[currentSlide].created);
    }
    return null;
  }, [comments, currentSlide]);

  const getMoreComments = () => {
    setLoading(true);
    fetchComments();
  };

  React.useEffect(() => {
    if (
      (currentSlide === 0 && comments.length === 0) ||
      currentSlide === comments.length - 10
    ) {
      fetchComments();
    }
  }, [currentSlide]);

  React.useEffect(() => {
    fetchChartByTicket(1);
  }, []);

  useEventListener("keydown", listenKeyboardDown);

  return (
    <div className={styles.container}>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div
          className={styles.carouselContainer}
          style={{ flex: 4, minHeight: "50vh" }}
        >
          <Carousel
            selectedItem={currentSlide}
            showStatus={false}
            showIndicators={false}
            onChange={handleSwipe}
          >
            {comments.map((comment, index) => (
              <div key={`${comment?.id}${index}`} className={styles.card}>
                <div className={styles.author}>{comment?.author}</div>
                <div className={styles.commentBody}>{comment?.body}</div>
                <h3 className={styles.dateText}>
                  {unixToDate(comment?.created)}
                </h3>
                <div className={styles.score}>score: {comment?.score}</div>
              </div>
            ))}
          </Carousel>
          {loadingChart ? (
            <div>Loading...</div>
          ) : (
            <div style={{ flex: 1 }}>
              <CandleChart
                dataChart={dataChart}
                loading={loadingChart}
                commentDate={selectedCommentDate}
              />
            </div>
          )}
        </div>
      )}
      <Buttons pressedButton={keyboardBeingPressed}></Buttons>
    </div>
  );
};
