import React, { FC } from 'react';
import styles from './styles/Button.module.css';
import classNames from 'classnames';

type Props = {
  pressedButton: string;
  button: string;
  predictionNumber: number;
};

export const Button: FC<Props> = ({
  pressedButton,
  button,
  predictionNumber,
}: Props) => {
  const isPressed =
    pressedButton === predictionNumber.toString() ||
    (button === 'delete' && pressedButton === 'd');

  return (
    <div className={styles.container}>
      <div>{predictionNumber === 4 ? 'D' : predictionNumber}</div>
      <div
        className={classNames(styles.button, {
          [styles.selected]: isPressed,
        })}
      >
        {button}
      </div>
    </div>
  );
};
