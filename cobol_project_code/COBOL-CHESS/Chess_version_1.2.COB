      ******************************************************************
      * Author: Anton Bystedt
      * Date: 2022-02-16
      * Purpose: Practicing COBOL logic
      * Tectonics: cobc
      ******************************************************************
      * THIS PROGRAM IS A CHESS PROGRAM WRITTEN IN THE WONDERFUL       *
      * LANGUAGE OF COBOL!                                             *
      ******************************************************************
       IDENTIFICATION DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       PROGRAM-ID. CHESS-V1.

       ENVIRONMENT DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       CONFIGURATION SECTION.
      *-----------------------
       INPUT-OUTPUT SECTION.
      *-----------------------
       DATA DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       FILE SECTION.
      *-----------------------
       WORKING-STORAGE SECTION.

           01 BRD-WIDTH    PIC X(27)
           VALUE '  A  B  C  D  E  F  G  H  '.

           01 BRD-ICON.
               05 BRD-ROWS PIC X(27) OCCURS 8 TIMES.

           01 WS-COUNTERS.
               05 WS-COUNTER   PIC 9.
               05 T-COUNTER    PIC 99.
               05 U-COUNTER    PIC 99.
               05 V-COUNTER    PIC 99.
               05 W-COUNTER    PIC 99.
               05 X-COUNTER    PIC 99.
               05 Y-COUNTER    PIC 99.
               05 Z-COUNTER    PIC 99.

           01 INPUT-VARIABLES.
               05 INPUT-VARIABLE       PIC X(2).
               05 INPUT-X-VARIABLE     PIC X(1).
               05 INPUT-X-VARIABLE-N   PIC S9(1).
               05 INPUT-Y-VARIABLE     PIC S9(1).
               05 START-INPUT          PIC X(1).

           01 WINNER-SWITCH        PIC X(1).
               88 W-WINNER     VALUE IS 'W'.
               88 B-WINNER     VALUE IS 'B'.
               88 NO-WINNER    VALUE IS 'N'.

           01 VALID-MOVE           PIC X(1).
               88 IS-VALID     VALUE 'Y'.
               88 NOT-VALID    VALUE 'N'.

           01 PLAYER-TURN          PIC X(1).
               88 W-TURN       VALUE 'W'.
               88 B-TURN       VALUE 'B'.

           01 TYPE-MOVE            PIC X(3).
               88 N-MO         VALUE 'NMO'.
               88 D-L-U        VALUE 'DLU'.
               88 D-R-U        VALUE 'DRU'.
               88 D-L-D        VALUE 'DLD'.
               88 D-R-D        VALUE 'DRD'.
               88 S-UP         VALUE 'SUP'.
               88 S-DN         VALUE 'SDN'.
               88 S-RI         VALUE 'SRI'.
               88 S-LE         VALUE 'SLE'.
               88 H-U-R        VALUE 'HUR'.
               88 H-U-L        VALUE 'HUL'.
               88 H-R-U        VALUE 'HRU'.
               88 H-L-U        VALUE 'HLU'.
               88 H-D-R        VALUE 'HDR'.
               88 H-D-L        VALUE 'HDL'.
               88 H-R-D        VALUE 'HRD'.
               88 H-L-D        VALUE 'HLD'.

           COPY COORDINATES.

      *-----------------------
       PROCEDURE DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       MAIN-PROCEDURE.
           PERFORM A-INITIALIZE
           PERFORM B-MAIN
           .

           A-INITIALIZE SECTION.

      *******************************************************************
      *                        A-INITIALIZE SECTION                     *
      *******************************************************************

               INITIALIZE WS-COUNTERS
               SET NO-WINNER TO TRUE
               MOVE 'W' TO PLAYER-TURN
               SET N-MO TO TRUE

           .


           B-MAIN SECTION.

      *******************************************************************
      *                         B-MAIN SECTION                          *
      *******************************************************************

           PERFORM BA-START-GAME
           PERFORM C-DISP-BOARD
           PERFORM D-CHECK-KING
           PERFORM GA-ACCEPT-CORD

           PERFORM UNTIL WINNER-SWITCH IS NOT = 'N'

               PERFORM CC-MOVE
               PERFORM D-CHECK-KING
               SET B-TURN TO TRUE
               PERFORM GA-ACCEPT-CORD

               PERFORM CC-MOVE
               PERFORM D-CHECK-KING
               SET W-TURN TO TRUE
               PERFORM GA-ACCEPT-CORD

           END-PERFORM

           STOP RUN.

           .

           BA-START-GAME SECTION.

      *******************************************************************
      *                       BA-START-GAME SECTION                     *
      *******************************************************************

           DISPLAY 'NEW GAME OR RESUME SAVED GAME?'
           DISPLAY    " "
           DISPLAY   'WRITE "N", FOR A NEW GAME OR "S" TO RESUME A GAME'
           ACCEPT START-INPUT

           MOVE FUNCTION UPPER-CASE (START-INPUT)
               TO START-INPUT
           EVALUATE START-INPUT
           WHEN 'N'
               CALL 'CSUB001' USING COORDINATES
           WHEN 'S'
               CALL 'CSUB002' USING COORDINATES
                                    PLAYER-TURN
           WHEN OTHER
               DISPLAY "ENTER A VALID VALUE."
               PERFORM BA-START-GAME
           END-EVALUATE
           .

           C-DISP-BOARD SECTION.

      *******************************************************************
      *                        C-DISP-BOARD SECTION                     *
      *******************************************************************

           MOVE 1 TO WS-COUNTER

           PERFORM UNTIL WS-COUNTER > 8

               MOVE '1 -- -- -- -- -- -- -- -- 1' TO
               BRD-ROWS(WS-COUNTER)

               PERFORM CA-COMPUTE

               PERFORM CB-MOVE

               MOVE WS-COUNTER TO BRD-ROWS(WS-COUNTER)(1:1)
               MOVE WS-COUNTER TO BRD-ROWS(WS-COUNTER)(27:1)

               ADD 1 TO WS-COUNTER

           END-PERFORM

           .

           CA-COMPUTE SECTION.

      *******************************************************************
      *                        CA-COMPUTE SECTION                       *
      *******************************************************************

           MOVE 1 TO T-COUNTER

           PERFORM UNTIL T-COUNTER > 16
               COMPUTE W-X-POS(T-COUNTER)
                       = (W-X-VAR(T-COUNTER) * 3)

               COMPUTE B-X-POS(T-COUNTER)
                       = (B-X-VAR(T-COUNTER) * 3)


               ADD 1 TO T-COUNTER
           END-PERFORM

           .

           CB-MOVE SECTION.

      *******************************************************************
      *                        CB-MOVE SECTION                          *
      *******************************************************************

           MOVE 1 TO T-COUNTER

           PERFORM UNTIL T-COUNTER >= 17

              IF PLAYER-TURN = 'B'
                 IF W-Y-POS(T-COUNTER) = WS-COUNTER
                    MOVE W-PIECE(T-COUNTER) TO
                    BRD-ROWS(WS-COUNTER)(W-X-POS(T-COUNTER):2)
                 END-IF
                 IF B-Y-POS(T-COUNTER) = WS-COUNTER
                    MOVE B-PIECE(T-COUNTER) TO
                    BRD-ROWS(WS-COUNTER)(B-X-POS(T-COUNTER):2)
                 END-IF
              END-IF
              IF PLAYER-TURN = 'W'
                 IF B-Y-POS(T-COUNTER) = WS-COUNTER
                    MOVE B-PIECE(T-COUNTER) TO
                    BRD-ROWS(WS-COUNTER)(B-X-POS(T-COUNTER):2)
                 END-IF
                 IF W-Y-POS(T-COUNTER) = WS-COUNTER
                    MOVE W-PIECE(T-COUNTER) TO
                    BRD-ROWS(WS-COUNTER)(W-X-POS(T-COUNTER):2)
                 END-IF

              END-IF

              ADD 1 TO T-COUNTER



           END-PERFORM
           .

           CC-MOVE SECTION.

      *******************************************************************
      *                          CC-MOVE SECTION                        *
      *******************************************************************

               PERFORM CA-COMPUTE
      *         DISPLAY "PERFORMING CC-MOVE"
               IF PLAYER-TURN = 'B'
                   MOVE B-PIECE(U-COUNTER) TO
                   BRD-ROWS(B-Y-POS(U-COUNTER))(B-X-POS(U-COUNTER):2)
               ELSE IF PLAYER-TURN = 'W'
                   MOVE W-PIECE(U-COUNTER) TO
                   BRD-ROWS(W-Y-POS(U-COUNTER))(W-X-POS(U-COUNTER):2)
               END-IF

           .

           D-CHECK-KING SECTION.

      *******************************************************************
      *                        D-CHECK-KING SECTION                     *
      *******************************************************************


           IF  B-PIECE(1) IS NOT = 'BK'
               AND PLAYER-TURN = 'W'
               SET W-WINNER TO TRUE
               PERFORM FA-NEW-BOARD
           DISPLAY " __      __  __  __  ______  ______  ____        __"
           "  __  ______   ____    ______  _____   ____    __    __"
           DISPLAY "/\ \  __/\ \/\ \/\ \/\__  _\/\__  _\/\  _`\     /\ "
           "\/\ \/\__  _\ /\  _`\ /\__  _\/\  __`\/\  _`\ /\ \  /\ \"
           DISPLAY "\ \ \/\ \ \ \ \ \_\ \/_/\ \/\/_/\ \/\ \ \L\_\   \ \"
           " \ \ \/_/\ \/ \ \ \/\_\/_/\ \/\ \ \/\ \ \ \L\ \ `\`\\/'/"
           DISPLAY " \ \ \ \ \ \ \ \  _  \ \ \ \   \ \ \ \ \  _\L    \ "
           "\ \ \ \ \ \ \  \ \ \/_/_ \ \ \ \ \ \ \ \ \ ,  /`\ `\ /'"
           DISPLAY "  \ \ \_/ \_\ \ \ \ \ \ \_\ \__ \ \ \ \ \ \L\ \   \"
           " \ \_/ \ \_\ \__\ \ \L\ \ \ \ \ \ \ \_\ \ \ \\ \ `\ \ \"
           DISPLAY "   \ `\___x___/\ \_\ \_\/\_____\ \ \_\ \ \____/    "
           "\ `\___/ /\_____\\ \____/  \ \_\ \ \_____\ \_\ \_\ \ \_\"
           DISPLAY "    '\/__//__/  \/_/\/_/\/_____/  \/_/  \/___/     "
           " `\/__/  \/_____/ \/___/    \/_/  \/_____/\/_/\/ /  \/_/"

               GOBACK
           ELSE IF W-PIECE(1) IS NOT = 'WK'
               AND PLAYER-TURN = 'B'
               SET B-WINNER TO TRUE
               PERFORM FA-NEW-BOARD
           DISPLAY " ____     __       ______  ____     __  __      __ "
           " __  ______   ____    ______  _____   ____    __    __"
           DISPLAY "/\  _`\  /\ \     /\  _  \/\  _`\  /\ \/\ \    /\ \"
           "/\ \/\__  _\ /\  _`\ /\__  _\/\  __`\/\  _`\ /\ \  /\ \"
           DISPLAY "\ \ \L\ \\ \ \    \ \ \L\ \ \ \/\_\\ \ \/'/'   \ \ "
           "\ \ \/_/\ \/ \ \ \/\_\/_/\ \/\ \ \/\ \ \ \L\ \ `\`\\/'/"
           DISPLAY " \ \  _ <'\ \ \  __\ \  __ \ \ \/_/_\ \ , <     \ \"
           " \ \ \ \ \ \  \ \ \/_/_ \ \ \ \ \ \ \ \ \ ,  /`\ `\ /'"
           DISPLAY "  \ \ \L\ \\ \ \L\ \\ \ \/\ \ \ \L\ \\ \ \\`\    \ "
           "\ \_/ \ \_\ \__\ \ \L\ \ \ \ \ \ \ \_\ \ \ \\ \ `\ \ \"
           DISPLAY "   \ \____/ \ \____/ \ \_\ \_\ \____/ \ \_\ \_\   \"
           " `\___/ /\_____\\ \____/  \ \_\ \ \_____\ \_\ \_\ \ \_\"
           DISPLAY "    \/___/   \/___/   \/_/\/_/\/___/   \/_/\/_/    "
           "`\/__/  \/_____/ \/___/    \/_/  \/_____/\/_/\/ /  \/_/"
               GOBACK
           END-IF

           .

           FA-NEW-BOARD SECTION.

      *******************************************************************
      *                        FA-NEW-BOARD SECTION                     *
      *******************************************************************

               DISPLAY " "
               DISPLAY " "

               MOVE 1 TO WS-COUNTER


               DISPLAY BRD-WIDTH

               PERFORM UNTIL WS-COUNTER > 8
                   DISPLAY  BRD-ROWS(WS-COUNTER)
                   DISPLAY " "
                   ADD 1 TO WS-COUNTER
               END-PERFORM

               DISPLAY BRD-WIDTH
               DISPLAY " "
           .

           GA-ACCEPT-CORD SECTION.

      *******************************************************************
      *                      GA-ACCEPT-CORD SECTION                     *
      *******************************************************************

           SET NOT-VALID TO TRUE
           SET N-MO TO TRUE
           PERFORM FA-NEW-BOARD
           EVALUATE PLAYER-TURN
           WHEN 'W'
               PERFORM UNTIL VALID-MOVE ='Y'
                   DISPLAY " "
                   DISPLAY 'SELECT YOUR WHITE PIECE OR ENTER S TO SAVE'
                   ' THE GAME'
                   ACCEPT INPUT-VARIABLE

                   PERFORM GAA-MOVE-INPUT

                   MOVE INPUT-VARIABLE(2:1) TO INPUT-Y-VARIABLE

                   PERFORM GAB-CHECK-VALID

               END-PERFORM

           WHEN 'B'
               PERFORM UNTIL VALID-MOVE ='Y'
                   DISPLAY " "
                   DISPLAY 'SELECT YOUR BLACK PIECE OR ENTER S TO SAVE'
                   ' THE GAME'

                   ACCEPT INPUT-VARIABLE

                   PERFORM GAA-MOVE-INPUT

                   MOVE INPUT-VARIABLE(2:1) TO INPUT-Y-VARIABLE

                   PERFORM GAB-CHECK-VALID

               END-PERFORM

           END-EVALUATE
           .

           GAA-MOVE-INPUT SECTION.

      *******************************************************************
      *                      GAA-MOVE-INPUT SECTION                     *
      *******************************************************************

           MOVE FUNCTION UPPER-CASE (INPUT-VARIABLE(1:1))
               TO INPUT-X-VARIABLE

           EVALUATE TRUE
           WHEN INPUT-X-VARIABLE = 'A'
               MOVE 1 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'B'
               MOVE 2 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'C'
               MOVE 3 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'D'
               MOVE 4 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'E'
               MOVE 5 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'F'
               MOVE 6 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'G'
               MOVE 7 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'H'
               MOVE 8 TO INPUT-X-VARIABLE-N
           WHEN INPUT-X-VARIABLE = 'S'
               CALL 'CSUB003' USING COORDINATES
                                    PLAYER-TURN
           WHEN OTHER
               DISPLAY "ENTER A VALID POSITION"
           END-EVALUATE


           .

           GAB-CHECK-VALID SECTION.

      *******************************************************************
      *                     GAB-CHECK-VALID SECTION                     *
      *******************************************************************

           MOVE 1 TO U-COUNTER

      **************************EVALUATE WHITE**************************

           EVALUATE TRUE
           WHEN PLAYER-TURN = 'W'
               PERFORM UNTIL  INPUT-X-VARIABLE-N = W-X-VAR(U-COUNTER)
                   AND INPUT-Y-VARIABLE = W-Y-POS(U-COUNTER)
                   OR U-COUNTER >= 16
                   ADD 1 TO U-COUNTER
               END-PERFORM

               EVALUATE TRUE
               WHEN W-PIECE(U-COUNTER) = '--'
                   SET NOT-VALID TO TRUE
                   DISPLAY "NO VALID PIECE HERE"
                   PERFORM GA-ACCEPT-CORD
               WHEN INPUT-Y-VARIABLE = W-Y-POS(U-COUNTER)
                   DISPLAY "YOU HAVE SELECTED " W-PIECE(U-COUNTER)
                           " IN POSITION " INPUT-X-VARIABLE
                           INPUT-Y-VARIABLE
                           PERFORM GAC-ACCEPT-MOVE
               WHEN OTHER
                   DISPLAY "NOBODOY HERE"
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

      **************************EVALUATE BLACK**************************

           WHEN PLAYER-TURN = 'B'
               PERFORM UNTIL  INPUT-X-VARIABLE-N = B-X-VAR(U-COUNTER)
                   AND INPUT-Y-VARIABLE = B-Y-POS(U-COUNTER)
                   OR U-COUNTER >= 16
                   ADD 1 TO U-COUNTER
               END-PERFORM

               EVALUATE TRUE
               WHEN B-PIECE(U-COUNTER) = '--'
                   SET NOT-VALID TO TRUE
                   DISPLAY "NO VALID PIECE HERE"
                   PERFORM GA-ACCEPT-CORD
               WHEN INPUT-Y-VARIABLE = B-Y-POS(U-COUNTER)
                   DISPLAY "YOU HAVE SELECTED " B-PIECE(U-COUNTER)
                           " IN POSITION " INPUT-X-VARIABLE
                           INPUT-Y-VARIABLE
                           PERFORM GAC-ACCEPT-MOVE
               WHEN OTHER
                   DISPLAY "NOBODOY HERE"
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

           END-EVALUATE
           .

           GAC-ACCEPT-MOVE SECTION.

      *******************************************************************
      *                     GAC-ACCEPT-MOVE SECTION                     *
      *******************************************************************

           SET NOT-VALID TO TRUE

           MOVE '|' TO BRD-ROWS(INPUT-Y-VARIABLE)
           (((INPUT-X-VARIABLE-N * 3) - 1):1)
           MOVE '|' TO BRD-ROWS(INPUT-Y-VARIABLE)
           (((INPUT-X-VARIABLE-N * 3) + 2):1)

           PERFORM FA-NEW-BOARD

           PERFORM UNTIL VALID-MOVE ='Y'

               MOVE ' ' TO BRD-ROWS(INPUT-Y-VARIABLE)
               (((INPUT-X-VARIABLE-N * 3) - 1):1)
               MOVE ' ' TO BRD-ROWS(INPUT-Y-VARIABLE)
               (((INPUT-X-VARIABLE-N * 3) + 2):1)


               DISPLAY 'MOVE THIS PIECE TO?'
               ACCEPT INPUT-VARIABLE

               PERFORM GAA-MOVE-INPUT

               MOVE INPUT-VARIABLE(2:1) TO INPUT-Y-VARIABLE

               PERFORM GAD-CHECK-MOVE


           END-PERFORM
           .

           GAD-CHECK-MOVE SECTION.

      *******************************************************************
      *                      GAD-CHECK-MOVE SECTION                     *
      *******************************************************************

      **************************EVALUATE WHITE***************************

           EVALUATE TRUE
           WHEN PLAYER-TURN = 'W'
               EVALUATE TRUE
               WHEN (W-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N) =
               (W-Y-POS(U-COUNTER) - INPUT-Y-VARIABLE) AND
               (W-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N >=0)
               AND TYPE-MOVE = 'NMO'

                   SET D-L-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER)) =
               (W-Y-POS(U-COUNTER)- INPUT-Y-VARIABLE) AND
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER) >=0 )
               AND TYPE-MOVE = 'NMO'

                   SET D-R-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
              (W-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N) =
              (INPUT-Y-VARIABLE - W-Y-POS(U-COUNTER))
              AND TYPE-MOVE = 'NMO'

                   SET D-L-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER) ) =
               (INPUT-Y-VARIABLE - W-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   SET D-R-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N = W-X-VAR(U-COUNTER) AND
               INPUT-Y-VARIABLE IS NOT = W-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   IF INPUT-Y-VARIABLE > W-Y-POS(U-COUNTER)
                       SET S-DN TO TRUE
                       SET IS-VALID TO TRUE
                   ELSE IF INPUT-Y-VARIABLE < W-Y-POS(U-COUNTER)
                       SET S-UP TO TRUE
                       SET IS-VALID TO TRUE
                   END-IF

                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N IS NOT = W-X-VAR(U-COUNTER) AND
               INPUT-Y-VARIABLE = W-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   IF INPUT-X-VARIABLE-N > W-X-VAR(U-COUNTER)
                       SET S-RI TO TRUE
                       SET IS-VALID TO TRUE
                   ELSE IF INPUT-X-VARIABLE-N < W-X-VAR(U-COUNTER)
                       SET S-LE TO TRUE
                       SET IS-VALID TO TRUE
                   END-IF


               WHEN U-COUNTER = 6 OR 5
                   SET IS-VALID TO TRUE
               WHEN OTHER
                   DISPLAY "INVALID MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

      **************************EVALUATE BLACK**************************

           WHEN PLAYER-TURN = 'B'

               EVALUATE TRUE
               WHEN (B-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N) =
               (B-Y-POS(U-COUNTER)- INPUT-Y-VARIABLE) AND
               (B-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N >=0)
               AND TYPE-MOVE = 'NMO'

                   SET D-L-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N - B-X-VAR(U-COUNTER)) =
               (B-Y-POS(U-COUNTER)- INPUT-Y-VARIABLE) AND
               INPUT-X-VARIABLE-N -(B-X-VAR(U-COUNTER)) >=0
               AND TYPE-MOVE = 'NMO'

                   SET D-R-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
              (B-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N) =
              (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER))
              AND TYPE-MOVE = 'NMO'

                   SET D-L-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N - B-X-VAR(U-COUNTER) ) =
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   SET D-R-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N = B-X-VAR(U-COUNTER) AND
               INPUT-Y-VARIABLE IS NOT = B-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   IF INPUT-Y-VARIABLE > B-Y-POS(U-COUNTER)
                       SET S-DN TO TRUE
                       SET IS-VALID TO TRUE
                   ELSE IF INPUT-Y-VARIABLE < B-Y-POS(U-COUNTER)
                       SET S-UP TO TRUE
                       SET IS-VALID TO TRUE
                   END-IF

                   SET IS-VALID TO TRUE

               WHEN
               (INPUT-X-VARIABLE-N IS NOT = B-X-VAR(U-COUNTER) AND
               INPUT-Y-VARIABLE = B-Y-POS(U-COUNTER))
               AND TYPE-MOVE = 'NMO'

                   IF INPUT-X-VARIABLE-N > B-X-VAR(U-COUNTER)
                       SET S-RI TO TRUE
                       SET IS-VALID TO TRUE
                   ELSE IF INPUT-X-VARIABLE-N < B-X-VAR(U-COUNTER)
                       SET S-LE TO TRUE
                       SET IS-VALID TO TRUE
                   END-IF

               WHEN U-COUNTER = 6 OR 5
                   SET IS-VALID TO TRUE
               WHEN OTHER
                   DISPLAY "INVALID MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

           END-EVALUATE

           EVALUATE U-COUNTER
           WHEN 1
               PERFORM HA-CHECK-KING
           WHEN 2
               PERFORM HB-CHECK-QUEEN
           WHEN 3 THRU 4
              PERFORM HC-CHECK-ROOK
           WHEN 5 THRU 6
               PERFORM HD-CHECK-HORSE
           WHEN 7 THRU 8
               PERFORM HE-CHECK-BISHOP
           WHEN  9 THRU 17
               PERFORM HF-CHECK-PAWN
           END-EVALUATE
           .

           HA-CHECK-KING SECTION.


      *******************************************************************
      *                       HA-CHECK-KING SECTION                     *
      *******************************************************************

      **************************EVALUATE WHITE**************************

           EVALUATE TRUE
           WHEN PLAYER-TURN = 'W'
               EVALUATE TRUE
               WHEN
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER) > 1) OR
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER) < -1) OR
               (INPUT-Y-VARIABLE - W-Y-POS(U-COUNTER) > 1) OR
               (INPUT-Y-VARIABLE - W-Y-POS(U-COUNTER) < -1)
                   DISPLAY "INVALID MOVE, A KING CAN ONLY MOVE 1 IN "
                   "ANY DIRECTION"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD


      **************************EVALUATE BLACK**************************

           WHEN PLAYER-TURN = 'B'
               EVALUATE TRUE
               WHEN
               (INPUT-X-VARIABLE-N - B-X-VAR(U-COUNTER) > 1) OR
               (INPUT-X-VARIABLE-N - B-X-VAR(U-COUNTER) < -1) OR
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER) > 1) OR
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER) < -1)
                   DISPLAY "INVALID MOVE, A KING CAN ONLY MOVE 1 IN "
                   "ANY DIRECTION"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD
               END-EVALUATE

           END-EVALUATE

           IF VALID-MOVE = 'Y' AND TYPE-MOVE NOT = 'NMO'
               PERFORM IBA-CHECK-POS
           ELSE
               DISPLAY "INCORRECT MOVE"
               PERFORM GA-ACCEPT-CORD
           END-IF

           .

           HB-CHECK-QUEEN SECTION.

      *******************************************************************
      *                      HB-CHECK-QUEEN SECTION                     *
      *******************************************************************

           IF VALID-MOVE = 'Y' AND TYPE-MOVE NOT = 'NMO'
               PERFORM IBA-CHECK-POS
           ELSE
               DISPLAY "INCORRECT MOVE"
               PERFORM GA-ACCEPT-CORD
           END-IF

           .

           HC-CHECK-ROOK SECTION.

      *******************************************************************
      *                      HC-CHECK-ROOK SECTION                      *
      *******************************************************************


           EVALUATE TYPE-MOVE
           WHEN
           'SUP' WHEN 'SDN' WHEN 'SRI' WHEN 'SLE'
               PERFORM IBA-CHECK-POS
           WHEN OTHER
               DISPLAY "INVALID MOVE"
               PERFORM GA-ACCEPT-CORD
           END-EVALUATE

           .

           HD-CHECK-HORSE SECTION.

      *******************************************************************
      *                     HD-CHECK-HORSE SECTION                      *
      *******************************************************************

           SET N-MO TO TRUE

           EVALUATE TRUE

      **************************EVALUATE WHITE**************************

           WHEN PLAYER-TURN = 'W'

               EVALUATE TRUE
               WHEN (INPUT-X-VARIABLE-N - 1) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 2) = W-Y-POS(U-COUNTER)

                   SET H-U-R TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 1) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 2) = W-Y-POS(U-COUNTER)

                   SET H-U-L TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N - 2) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 1) = W-Y-POS(U-COUNTER)

                   SET H-R-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 2) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 1) = W-Y-POS(U-COUNTER)

                   SET H-L-U TO TRUE
                   SET IS-VALID TO TRUE

                WHEN (INPUT-X-VARIABLE-N - 1) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 2) = W-Y-POS(U-COUNTER)

                   SET H-D-R TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 1) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 2) = W-Y-POS(U-COUNTER)

                   SET H-D-L TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N - 2) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 1) = W-Y-POS(U-COUNTER)

                   SET H-R-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 2) = W-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 1) = W-Y-POS(U-COUNTER)

                   SET H-L-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN OTHER
                   DISPLAY "INVALID HORSE MOVE"
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

      **************************EVALUATE BLACK**************************

           WHEN PLAYER-TURN = 'B'
               EVALUATE TRUE
               WHEN (INPUT-X-VARIABLE-N - 1) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 2) = B-Y-POS(U-COUNTER)

                   SET H-U-R TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 1) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 2) = B-Y-POS(U-COUNTER)

                   SET H-U-L TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N - 2) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 1) = B-Y-POS(U-COUNTER)

                   SET H-R-U TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 2) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE + 1) = B-Y-POS(U-COUNTER)

                   SET H-L-U TO TRUE
                   SET IS-VALID TO TRUE

                WHEN (INPUT-X-VARIABLE-N - 1) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 2) = B-Y-POS(U-COUNTER)

                   SET H-D-R TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 1) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 2) = B-Y-POS(U-COUNTER)

                   SET H-D-L TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N - 2) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 1) = B-Y-POS(U-COUNTER)

                   SET H-R-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN (INPUT-X-VARIABLE-N + 2) = B-X-VAR(U-COUNTER)
                   AND (INPUT-Y-VARIABLE - 1) = B-Y-POS(U-COUNTER)

                   SET H-L-D TO TRUE
                   SET IS-VALID TO TRUE

               WHEN OTHER
                   DISPLAY "INVALID HORSE MOVE"
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

           END-EVALUATE

           IF VALID-MOVE = 'Y' AND TYPE-MOVE NOT = 'NMO'
               PERFORM IBA-CHECK-POS
           END-IF


           .

           HE-CHECK-BISHOP SECTION.

      *******************************************************************
      *                    HE-CHECK-BISHOP SECTION                      *
      *******************************************************************

           EVALUATE TYPE-MOVE
           WHEN 'SUP' WHEN 'SDN' WHEN 'SRI' WHEN 'SLE'
               PERFORM IBA-CHECK-POS
           WHEN OTHER
               DISPLAY "INVALID MOVE"
               SET NOT-VALID TO TRUE
               PERFORM GA-ACCEPT-CORD
           END-EVALUATE
           .

           HF-CHECK-PAWN SECTION.

      *******************************************************************
      *                      HF-CHECK-PAWN SECTION                      *
      *******************************************************************

           EVALUATE TRUE

      **************************EVALUATE WHITE**************************

           WHEN PLAYER-TURN = 'W'
               EVALUATE TRUE
               WHEN
               W-FIRST(U-COUNTER) = 'Y' AND
               (W-Y-POS(U-COUNTER) - INPUT-Y-VARIABLE > 2)

                   DISPLAY "INVALID MOVE, A PAWN CAN ONLY MOVE 2 "
                   "ON FIRST MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               WHEN
               W-FIRST(U-COUNTER) = 'N' AND
               (W-Y-POS(U-COUNTER) - INPUT-Y-VARIABLE  > 1)

                   DISPLAY "INVALID MOVE, A PAWN CAN ONLY MOVE 1 "
                   "AFTER FIRST MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               WHEN TYPE-MOVE = 'DLU' AND
               (W-Y-POS(U-COUNTER) - INPUT-Y-VARIABLE  = 1)
               AND
               (W-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N  = 1)
                   SET IS-VALID TO TRUE

               WHEN TYPE-MOVE = 'DRU' AND
               (W-Y-POS(U-COUNTER) - INPUT-Y-VARIABLE = 1 )
               AND
               (INPUT-X-VARIABLE-N - W-X-VAR(U-COUNTER) = 1)

                   SET IS-VALID TO TRUE

               WHEN TYPE-MOVE = 'SUP'
                   SET IS-VALID TO TRUE

               WHEN OTHER
                   DISPLAY "INVALID MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE

      **************************EVALUATE BLACK**************************

           WHEN PLAYER-TURN = 'B'
               EVALUATE TRUE
               WHEN
               B-FIRST(U-COUNTER) = 'Y' AND
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER) > 2)

                   DISPLAY "INVALID MOVE, A PAWN CAN ONLY MOVE 2 "
                   "ON FIRST MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               WHEN
               B-FIRST(U-COUNTER) = 'N' AND
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER) > 1)

                   DISPLAY "INVALID MOVE, A PAWN CAN ONLY MOVE 1 "
                   "AFTER FIRST MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               WHEN TYPE-MOVE = 'DLD' AND
               (INPUT-Y-VARIABLE - B-Y-POS(U-COUNTER) = 1)
               AND
               (B-X-VAR(U-COUNTER) - INPUT-X-VARIABLE-N  = 1)

                       SET IS-VALID TO TRUE

               WHEN TYPE-MOVE = 'DRD' AND
               (INPUT-Y-VARIABLE- B-Y-POS(U-COUNTER)  = 1 )
               AND
               (INPUT-X-VARIABLE-N - B-X-VAR(U-COUNTER) = 1)

                   SET IS-VALID TO TRUE

               WHEN TYPE-MOVE = 'SDN'

                   SET IS-VALID TO TRUE

               WHEN OTHER
                   DISPLAY "INVALID MOVE"
                   SET NOT-VALID TO TRUE
                   PERFORM GA-ACCEPT-CORD

               END-EVALUATE


           END-EVALUATE

           IF VALID-MOVE = 'Y' AND TYPE-MOVE NOT = 'NMO'
               PERFORM IBA-CHECK-POS
           END-IF


           .

           IBA-CHECK-POS SECTION.

      *******************************************************************
      *                       IBA-CHECK-POS SECTION                     *
      *******************************************************************

           MOVE 1 TO V-COUNTER
           MOVE 1 TO W-COUNTER

           EVALUATE TRUE
           WHEN PLAYER-TURN = 'W'
           PERFORM IBAA-CHECK-WHITE

           WHEN PLAYER-TURN = 'B'
           PERFORM IBAB-CHECK-BLACK

           END-EVALUATE

           .

           IBAA-CHECK-WHITE SECTION.

      *******************************************************************
      *                    IBAA-CHECK-WHITE SECTION                     *
      *******************************************************************

      **************************EVALUATE WHITE***************************

           PERFORM UNTIL INPUT-X-VARIABLE-N = W-X-VAR(V-COUNTER)
               AND INPUT-Y-VARIABLE = W-Y-POS(V-COUNTER)
               OR V-COUNTER >= 16
               ADD 1 TO V-COUNTER
           END-PERFORM

           PERFORM UNTIL INPUT-X-VARIABLE-N = B-X-VAR(W-COUNTER)
               AND INPUT-Y-VARIABLE = B-Y-POS(W-COUNTER)
               OR W-COUNTER >= 16
               ADD 1 TO W-COUNTER
           END-PERFORM

           MOVE INPUT-X-VARIABLE-N TO X-COUNTER
           MOVE INPUT-Y-VARIABLE TO Y-COUNTER

           EVALUATE TRUE

           WHEN TYPE-MOVE ='DRU'

                   IF W-PIECE(U-COUNTER) = 'WP'
                       IF INPUT-Y-VARIABLE NOT = B-Y-POS(W-COUNTER)
                         AND INPUT-X-VARIABLE-N NOT = B-X-VAR(W-COUNTER)

                           DISPLAY "INVALID PAWN MOVE"
                           PERFORM GA-ACCEPT-CORD

                       END-IF
                   END-IF

               PERFORM UNTIL X-COUNTER >= W-X-VAR(U-COUNTER)
                   AND Y-COUNTER >= W-Y-POS(U-COUNTER) OR
                   X-COUNTER = 0
                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER

                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "DIAGONALLY UP TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                   ADD 1 TO Z-COUNTER


                   END-PERFORM

                   ADD 1 TO Y-COUNTER
                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE ='DLU'

                   IF W-PIECE(U-COUNTER) = 'WP'
                       IF INPUT-Y-VARIABLE NOT = B-Y-POS(W-COUNTER)
                         AND INPUT-X-VARIABLE-N NOT = B-X-VAR(W-COUNTER)

                           DISPLAY "INVALID PAWN MOVE"
                           PERFORM GA-ACCEPT-CORD
                       END-IF
                   END-IF

               PERFORM UNTIL X-COUNTER >= W-X-VAR(U-COUNTER)
                       AND Y-COUNTER >= W-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "DIAGONALLY UP TO THE LEFT"
                           PERFORM GA-ACCEPT-CORD

                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO Y-COUNTER
                   ADD 1 TO X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'DLD'

                   PERFORM UNTIL X-COUNTER >= W-X-VAR(U-COUNTER)
                       AND Y-COUNTER >= W-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "DIAGONALLY DOWN TO THE LEFT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM Y-COUNTER
                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'DRD'

               PERFORM UNTIL X-COUNTER >= W-X-VAR(U-COUNTER)
                       AND Y-COUNTER <= W-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "DIAGONALLY DOWN TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                       END-PERFORM

                   SUBTRACT 1 FROM Y-COUNTER
                   ADD 1 TO X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SUP'

               IF W-PIECE(U-COUNTER) = 'WP'
                   IF INPUT-Y-VARIABLE = B-Y-POS(W-COUNTER)
                     AND INPUT-X-VARIABLE-N = B-X-VAR(W-COUNTER)

                       DISPLAY "INVALID PAWN MOVE"
                       PERFORM GA-ACCEPT-CORD

                   END-IF
               END-IF

               PERFORM UNTIL X-COUNTER = W-X-VAR(U-COUNTER)
                       AND Y-COUNTER = W-Y-POS(U-COUNTER) OR
                       Y-COUNTER > 8

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "ABOVE"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO Y-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SDN'
               PERFORM UNTIL X-COUNTER = W-X-VAR(U-COUNTER)
                       AND Y-COUNTER = W-Y-POS(U-COUNTER) OR
                       Y-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "BENEATH"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM Y-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE ='SRI'
               PERFORM UNTIL X-COUNTER = W-X-VAR(U-COUNTER)
                       AND Y-COUNTER = W-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SLE'
               PERFORM UNTIL X-COUNTER = W-X-VAR(U-COUNTER)
                       AND Y-COUNTER = W-Y-POS(U-COUNTER) OR
                       X-COUNTER > 8

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF W-X-VAR(Z-COUNTER) = X-COUNTER
                           AND W-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, WHITE PIECE "
                           "TO THE LEFT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO X-COUNTER

               END-PERFORM
               WHEN OTHER
                   CONTINUE

           END-EVALUATE

           IF INPUT-Y-VARIABLE = W-Y-POS(V-COUNTER)
               AND INPUT-X-VARIABLE-N = W-X-VAR(V-COUNTER)
               AND TYPE-MOVE NOT = 'NMO'
               DISPLAY "INVALID MOVE: WHITE PIECE HERE"
               SET NOT-VALID TO TRUE
               PERFORM GA-ACCEPT-CORD

           ELSE IF INPUT-Y-VARIABLE = B-Y-POS(W-COUNTER)
               AND INPUT-X-VARIABLE-N = B-X-VAR(W-COUNTER)
               AND TYPE-MOVE NOT = 'NMO'
               MOVE '--' TO B-PIECE(W-COUNTER)
               MOVE 0 TO B-X-POS(W-COUNTER)
               MOVE 0 TO B-Y-POS(W-COUNTER)
               PERFORM IBB-MOVE-POS
           ELSE
               SET IS-VALID TO TRUE
               PERFORM IBB-MOVE-POS
           END-IF

           .

           IBAB-CHECK-BLACK SECTION.

      *******************************************************************
      *                    IBAB-CHECK-BLACK SECTION                     *
      *******************************************************************

      **************************EVALUATE BLACK***************************

           DISPLAY "CHECKING BLACK"
           PERFORM UNTIL INPUT-X-VARIABLE-N = B-X-VAR(V-COUNTER)
                         AND INPUT-Y-VARIABLE = B-Y-POS(V-COUNTER)
                         OR V-COUNTER >= 16
               ADD 1 TO V-COUNTER
           END-PERFORM

           PERFORM UNTIL INPUT-X-VARIABLE-N = W-X-VAR(W-COUNTER)
                         AND INPUT-Y-VARIABLE = W-Y-POS(W-COUNTER)
                         OR W-COUNTER >= 16
               ADD 1 TO W-COUNTER
           END-PERFORM

           MOVE INPUT-X-VARIABLE-N TO X-COUNTER
           MOVE INPUT-Y-VARIABLE TO Y-COUNTER

           EVALUATE TRUE
           WHEN TYPE-MOVE = 'DRU'
               PERFORM UNTIL X-COUNTER >= B-X-VAR(U-COUNTER)
                             AND Y-COUNTER >= B-Y-POS(U-COUNTER) OR
                             X-COUNTER = 0
                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                          AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                                   "DIAGONALLY UP TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER


                   END-PERFORM

                   ADD 1 TO Y-COUNTER
                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'DLU'
               PERFORM UNTIL X-COUNTER >= B-X-VAR(U-COUNTER)
                             AND Y-COUNTER >= B-Y-POS(U-COUNTER) OR
                             X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                          AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                                   "DIAGONALLY UP TO THE LEFT"
                           PERFORM GA-ACCEPT-CORD

                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO Y-COUNTER
                   ADD 1 TO X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'DLD'

                   IF B-PIECE(U-COUNTER) = 'BP'
                       IF INPUT-Y-VARIABLE NOT = W-Y-POS(W-COUNTER)
                         AND INPUT-X-VARIABLE-N NOT = W-X-VAR(W-COUNTER)

                           DISPLAY "INVALID PAWN MOVE"
                           PERFORM GA-ACCEPT-CORD
                       END-IF
                   END-IF

                   PERFORM UNTIL X-COUNTER >= B-X-VAR(U-COUNTER)
                       AND Y-COUNTER >= B-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                       MOVE 1 TO Z-COUNTER

                       PERFORM UNTIL Z-COUNTER > 16

                           IF B-X-VAR(Z-COUNTER) = X-COUNTER
                               AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                               DISPLAY "INCORRECT MOVE, BLACK PIECE "
                               "DIAGONALLY DOWN TO THE LEFT"
                               PERFORM GA-ACCEPT-CORD
                           END-IF

                           PERFORM IBAC-CHECK-INFRONT

                           ADD 1 TO Z-COUNTER

                       END-PERFORM

                       SUBTRACT 1 FROM Y-COUNTER
                       ADD 1 TO X-COUNTER

                   END-PERFORM

           WHEN TYPE-MOVE = 'DRD'

               IF B-PIECE(U-COUNTER) = 'BP'
                   IF INPUT-Y-VARIABLE NOT = W-Y-POS(W-COUNTER)
                     AND INPUT-X-VARIABLE-N NOT = W-X-VAR(W-COUNTER)

                       DISPLAY "INVALID PAWN MOVE"
                       PERFORM GA-ACCEPT-CORD
                   END-IF
               END-IF

               PERFORM UNTIL X-COUNTER >= B-X-VAR(U-COUNTER)
                       AND Y-COUNTER <= B-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                           "DIAGONALLY DOWN TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM Y-COUNTER
                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SUP'

               PERFORM UNTIL X-COUNTER = B-X-VAR(U-COUNTER)
                       AND Y-COUNTER = B-Y-POS(U-COUNTER) OR
                       Y-COUNTER > 8

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                           "ABOVE"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO Y-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SDN'

               IF B-PIECE(U-COUNTER) = 'BP'
                   IF INPUT-Y-VARIABLE = W-Y-POS(W-COUNTER)
                     AND INPUT-X-VARIABLE-N = W-X-VAR(W-COUNTER)

                       DISPLAY "INVALID PAWN MOVE"
                       PERFORM GA-ACCEPT-CORD

                   END-IF
               END-IF


               PERFORM UNTIL X-COUNTER = B-X-VAR(U-COUNTER)
                       AND Y-COUNTER = B-Y-POS(U-COUNTER) OR
                       Y-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                           "BENEATH"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM Y-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SRI'

               PERFORM UNTIL X-COUNTER = B-X-VAR(U-COUNTER)
                       AND Y-COUNTER = B-Y-POS(U-COUNTER) OR
                       X-COUNTER = 0

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                           "TO THE RIGHT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   SUBTRACT 1 FROM X-COUNTER

               END-PERFORM

           WHEN TYPE-MOVE = 'SLE'

               PERFORM UNTIL X-COUNTER = B-X-VAR(U-COUNTER)
                       AND Y-COUNTER = B-Y-POS(U-COUNTER) OR
                       X-COUNTER > 8

                   MOVE 1 TO Z-COUNTER

                   PERFORM UNTIL Z-COUNTER > 16

                       IF B-X-VAR(Z-COUNTER) = X-COUNTER
                           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
                           DISPLAY "INCORRECT MOVE, BLACK PIECE "
                           "TO THE LEFT"
                           PERFORM GA-ACCEPT-CORD
                       END-IF

                       PERFORM IBAC-CHECK-INFRONT

                       ADD 1 TO Z-COUNTER

                   END-PERFORM

                   ADD 1 TO X-COUNTER

               END-PERFORM
           WHEN OTHER
               CONTINUE

           END-EVALUATE
           IF INPUT-Y-VARIABLE = B-Y-POS(V-COUNTER)
               AND INPUT-X-VARIABLE-N = B-X-VAR(V-COUNTER)
               AND TYPE-MOVE NOT = 'NMO'
               DISPLAY "INVALID MOVE: BLACK PIECE HERE"
               SET NOT-VALID TO TRUE
               PERFORM GA-ACCEPT-CORD

           ELSE IF INPUT-Y-VARIABLE = W-Y-POS(W-COUNTER)
               AND INPUT-X-VARIABLE-N = W-X-VAR(W-COUNTER)
               AND TYPE-MOVE NOT = 'NMO'
               MOVE '--' TO W-PIECE(W-COUNTER)
               MOVE 0 TO W-X-POS(W-COUNTER)
               MOVE 0 TO W-Y-POS(W-COUNTER)
               PERFORM IBB-MOVE-POS
           ELSE
               SET IS-VALID TO TRUE
               PERFORM IBB-MOVE-POS
           END-IF

           .

           IBAC-CHECK-INFRONT SECTION.

      *******************************************************************
      *                  IBAC-CHECK-INFRONT SECTION                     *
      *******************************************************************

           IF B-X-VAR(Z-COUNTER) = X-COUNTER
           AND B-Y-POS(Z-COUNTER) = Y-COUNTER
           AND (X-COUNTER NOT = INPUT-X-VARIABLE-N
           OR Y-COUNTER NOT = INPUT-Y-VARIABLE)

               DISPLAY "BLACK PIECE IN FRONT OF THE "
                   "WANTED POSITION"
               PERFORM GA-ACCEPT-CORD
           END-IF

           IF W-X-VAR(Z-COUNTER) = X-COUNTER
              AND W-Y-POS(Z-COUNTER) = Y-COUNTER
              AND X-COUNTER NOT = INPUT-X-VARIABLE-N
              AND Y-COUNTER NOT = INPUT-Y-VARIABLE

               DISPLAY "WHITE PIECE IN FRONT OF THE "
                       "WANTED POSITION"
               PERFORM GA-ACCEPT-CORD
           END-IF

           .

           IBB-MOVE-POS SECTION.

      *******************************************************************
      *                        IBB-MOVE-POS SECTION                     *
      *******************************************************************

           SET N-MO TO TRUE


           EVALUATE TRUE
           WHEN PLAYER-TURN = 'W'
               AND VALID-MOVE = 'Y'

               MOVE "--" TO
                   BRD-ROWS(W-Y-POS(U-COUNTER))(W-X-POS(U-COUNTER):2)
               MOVE INPUT-Y-VARIABLE TO W-Y-POS(U-COUNTER)
               MOVE INPUT-X-VARIABLE-N TO W-X-VAR(U-COUNTER)
               MOVE 'N' TO W-FIRST(U-COUNTER)

           WHEN PLAYER-TURN = 'B'
               AND VALID-MOVE = 'Y'

               MOVE "--" TO
                   BRD-ROWS(B-Y-POS(U-COUNTER))(B-X-POS(U-COUNTER):2)
               MOVE INPUT-Y-VARIABLE TO B-Y-POS(U-COUNTER)
               MOVE INPUT-X-VARIABLE-N TO B-X-VAR(U-COUNTER)
               MOVE 'N' TO B-FIRST(U-COUNTER)

           WHEN OTHER
               DISPLAY "ERROR"
               PERFORM GA-ACCEPT-CORD

           END-EVALUATE



           .
